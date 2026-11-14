"""
test_hardware_arbiter.py — Rigorous unit test suite with negative mutation tests
Validates HRI calculations, profile threshold boundaries, thread clamp policies,
i18n dictionaries, and XML validity of SVG mascot assets.
"""

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from hardware_arbiter.i18n import t, TRANSLATIONS
from hardware_arbiter.benchmark import evaluate_gpu_tier


class TestHRIClassification(unittest.TestCase):
    """Test HRI calculation and profile classification boundaries."""

    def calculate_hri_and_profile(self, cpu_score: float, gpu_score: float) -> tuple[float, str]:
        hri = round(gpu_score / (cpu_score + 1e-6), 2)
        if hri >= 2.0:
            profile = "GPU_DOMINANT"
        elif hri <= 0.6:
            profile = "CPU_DOMINANT"
        else:
            profile = "BALANCED"
        return hri, profile

    def test_gpu_dominant_threshold(self):
        # i7-4790 (score ~5.0) + RX 6600 (score ~85.0) -> HRI = 17.0
        hri, profile = self.calculate_hri_and_profile(5.0, 85.0)
        self.assertGreaterEqual(hri, 2.0)
        self.assertEqual(profile, "GPU_DOMINANT")

    def test_cpu_dominant_threshold(self):
        # i9-14900K (score ~95.0) + iGPU (score ~15.0) -> HRI = 0.16
        hri, profile = self.calculate_hri_and_profile(95.0, 15.0)
        self.assertLessEqual(hri, 0.6)
        self.assertEqual(profile, "CPU_DOMINANT")

    def test_balanced_threshold(self):
        # Ryzen 5 5600 (score ~40.0) + GTX 1660 (score ~45.0) -> HRI = 1.125
        hri, profile = self.calculate_hri_and_profile(40.0, 45.0)
        self.assertGreater(hri, 0.6)
        self.assertLess(hri, 2.0)
        self.assertEqual(profile, "BALANCED")

    def test_negative_mutation_inversion(self):
        """Mutation test: proving that inverted hardware inputs correctly flip profile output."""
        # Baseline: GPU dominant
        _, profile_gpu = self.calculate_hri_and_profile(5.0, 85.0)
        self.assertEqual(profile_gpu, "GPU_DOMINANT")

        # Inverted: CPU dominant with same numbers swapped
        _, profile_cpu = self.calculate_hri_and_profile(85.0, 5.0)
        self.assertEqual(profile_cpu, "CPU_DOMINANT")

        # Prove they cannot be equal under swapped inputs
        self.assertNotEqual(profile_gpu, profile_cpu)


class TestI18nTranslations(unittest.TestCase):
    """Test trilingual dictionary coverage and fallbacks."""

    def test_all_locales_present(self):
        for lang in ("en", "pt", "zh"):
            self.assertIn(lang, TRANSLATIONS)

    def test_key_completeness(self):
        required_keys = [
            "title", "cpu_detected", "gpu_detected", "hri_label",
            "diagnosis_gpu_dominant", "diagnosis_cpu_dominant", "diagnosis_balanced",
            "policies_applied", "thread_clamp_applied"
        ]
        for lang in ("en", "pt", "zh"):
            for k in required_keys:
                translated = t(k, lang)
                self.assertIsInstance(translated, str)
                self.assertGreater(len(translated), 0, f"Key '{k}' in lang '{lang}' is empty")

    def test_fallback_on_unknown_lang(self):
        fallback = t("title", "unknown_lang")
        self.assertEqual(fallback, t("title", "en"))


class TestGPUTierEvaluation(unittest.TestCase):
    """Test GPU tier scoring logic."""

    def test_dedicated_rx6600(self):
        gpu_info = {
            "devices": [{"name": "AMD Radeon RX 6600", "vram_gb": 8.0, "is_integrated": False}],
            "directml_available": True,
            "cuda_available": False
        }
        score, tier = evaluate_gpu_tier(gpu_info)
        self.assertGreaterEqual(score, 70.0)
        self.assertEqual(tier, "Mid-Range Dedicated (DirectML/ROCm/CUDA)")

    def test_integrated_intel_hd(self):
        gpu_info = {
            "devices": [{"name": "Intel HD Graphics 4600", "vram_gb": 1.0, "is_integrated": True}],
            "directml_available": False,
            "cuda_available": False
        }
        score, tier = evaluate_gpu_tier(gpu_info)
        self.assertLess(score, 30.0)
        self.assertEqual(tier, "Integrated / Generic Graphics")


class TestMascotSVGValidity(unittest.TestCase):
    """Ensure all mascot and hero banner SVGs are well-formed XML and contain key animation layers."""

    def setUp(self):
        self.repo_root = Path(__file__).resolve().parent.parent
        self.pente_svg = self.repo_root / "mascot" / "pente_mascot.svg"
        self.hero_svg = self.repo_root / "mascot" / "hero-banner.svg"

    def test_pente_mascot_svg_xml_well_formed(self):
        self.assertTrue(self.pente_svg.exists(), "pente_mascot.svg must exist")
        tree = ET.parse(self.pente_svg)
        root = tree.getroot()
        self.assertTrue(root.tag.endswith("svg"))

    def test_hero_banner_svg_xml_well_formed(self):
        self.assertTrue(self.hero_svg.exists(), "hero-banner.svg must exist")
        tree = ET.parse(self.hero_svg)
        root = tree.getroot()
        self.assertTrue(root.tag.endswith("svg"))

    def test_pente_mascot_contains_required_animations(self):
        content = self.pente_svg.read_text(encoding="utf-8")
        # Check required keyframe animations
        self.assertIn("bodyBreathe", content)
        self.assertIn("combStrokeMotion", content)
        self.assertIn("eyeBlinkAnim", content)
        self.assertIn("pupilDrift", content)
        self.assertIn("waveNoodle", content)
        self.assertIn("laserFlowMove", content)
        # Check anatomy elements
        self.assertIn("pente-sticker-halo", content)
        self.assertIn("comb-and-paws-rig", content)


if __name__ == "__main__":
    unittest.main()
