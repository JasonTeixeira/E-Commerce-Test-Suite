"""
Screenshot comparison utilities for visual regression testing.

Provides image comparison, diff generation, and threshold management
for detecting visual regressions across browsers and viewports.
"""

import os
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageChops, ImageDraw


class ScreenshotCompare:
    """Utility for comparing screenshots and detecting visual differences."""

    def __init__(self, baseline_dir: str = "visual/baselines", diff_dir: str = "visual/diffs"):
        """Initialize screenshot comparison utility.

        Args:
            baseline_dir: Directory for baseline screenshots
            diff_dir: Directory for diff images
        """
        self.baseline_dir = Path(baseline_dir)
        self.diff_dir = Path(diff_dir)
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self.diff_dir.mkdir(parents=True, exist_ok=True)

    def compare_images(
        self,
        image1_path: str,
        image2_path: str,
        threshold: float = 0.1,
        ignore_antialiasing: bool = True
    ) -> Tuple[bool, float]:
        """Compare two images and return similarity result.

        Args:
            image1_path: Path to first image (baseline)
            image2_path: Path to second image (current)
            threshold: Acceptable difference threshold (0.0-1.0)
            ignore_antialiasing: Whether to ignore minor pixel differences

        Returns:
            Tuple of (is_similar, difference_percentage)
        """
        img1 = Image.open(image1_path).convert("RGB")
        img2 = Image.open(image2_path).convert("RGB")

        # Ensure images are same size
        if img1.size != img2.size:
            return False, 1.0

        # Calculate pixel-by-pixel difference
        diff = ImageChops.difference(img1, img2)
        
        # Calculate difference percentage
        diff_pixels = sum(sum(pixel) for pixel in diff.getdata())
        total_pixels = img1.size[0] * img1.size[1] * 3 * 255  # RGB * max_value
        difference = diff_pixels / total_pixels

        is_similar = difference <= threshold

        return is_similar, difference

    def create_diff_image(
        self,
        baseline_path: str,
        current_path: str,
        output_path: str
    ) -> None:
        """Create a diff image highlighting differences.

        Args:
            baseline_path: Path to baseline image
            current_path: Path to current image
            output_path: Path to save diff image
        """
        baseline = Image.open(baseline_path).convert("RGB")
        current = Image.open(current_path).convert("RGB")

        if baseline.size != current.size:
            # Resize current to match baseline
            current = current.resize(baseline.size)

        # Create difference image
        diff = ImageChops.difference(baseline, current)

        # Enhance difference for visibility
        diff = diff.point(lambda x: x * 10)

        # Create side-by-side comparison
        width = baseline.size[0] * 3
        height = baseline.size[1]
        comparison = Image.new("RGB", (width, height))

        # Paste images
        comparison.paste(baseline, (0, 0))
        comparison.paste(current, (baseline.size[0], 0))
        comparison.paste(diff, (baseline.size[0] * 2, 0))

        # Add labels
        draw = ImageDraw.Draw(comparison)
        # Labels would need a font, skipping for simplicity

        comparison.save(output_path)

    def save_baseline(self, screenshot_path: str, name: str) -> str:
        """Save a screenshot as baseline.

        Args:
            screenshot_path: Path to screenshot to save
            name: Baseline name

        Returns:
            Path to saved baseline
        """
        baseline_path = self.baseline_dir / f"{name}.png"
        img = Image.open(screenshot_path)
        img.save(baseline_path)
        return str(baseline_path)

    def compare_with_baseline(
        self,
        screenshot_path: str,
        name: str,
        threshold: float = 0.1,
        save_diff: bool = True
    ) -> Tuple[bool, float, Optional[str]]:
        """Compare screenshot with baseline.

        Args:
            screenshot_path: Path to current screenshot
            name: Baseline name
            threshold: Acceptable difference threshold
            save_diff: Whether to save diff image

        Returns:
            Tuple of (is_similar, difference, diff_path)
        """
        baseline_path = self.baseline_dir / f"{name}.png"

        if not baseline_path.exists():
            # No baseline exists, save current as baseline
            self.save_baseline(screenshot_path, name)
            return True, 0.0, None

        is_similar, difference = self.compare_images(
            str(baseline_path),
            screenshot_path,
            threshold
        )

        diff_path = None
        if not is_similar and save_diff:
            diff_path = self.diff_dir / f"{name}_diff.png"
            self.create_diff_image(
                str(baseline_path),
                screenshot_path,
                str(diff_path)
            )

        return is_similar, difference, str(diff_path) if diff_path else None

    def update_baseline(self, screenshot_path: str, name: str) -> str:
        """Update baseline with new screenshot.

        Args:
            screenshot_path: Path to new baseline
            name: Baseline name

        Returns:
            Path to updated baseline
        """
        return self.save_baseline(screenshot_path, name)

    def compare_regions(
        self,
        image1_path: str,
        image2_path: str,
        region: Tuple[int, int, int, int],
        threshold: float = 0.1
    ) -> Tuple[bool, float]:
        """Compare specific regions of two images.

        Args:
            image1_path: Path to first image
            image2_path: Path to second image
            region: Tuple of (left, top, right, bottom)
            threshold: Acceptable difference threshold

        Returns:
            Tuple of (is_similar, difference)
        """
        img1 = Image.open(image1_path).convert("RGB")
        img2 = Image.open(image2_path).convert("RGB")

        # Crop to region
        region1 = img1.crop(region)
        region2 = img2.crop(region)

        # Save temporary cropped images
        temp_path1 = self.diff_dir / "temp_region1.png"
        temp_path2 = self.diff_dir / "temp_region2.png"

        region1.save(temp_path1)
        region2.save(temp_path2)

        # Compare regions
        result = self.compare_images(
            str(temp_path1),
            str(temp_path2),
            threshold
        )

        # Cleanup temp files
        temp_path1.unlink()
        temp_path2.unlink()

        return result

    def get_image_hash(self, image_path: str) -> str:
        """Get perceptual hash of image for quick comparison.

        Args:
            image_path: Path to image

        Returns:
            Image hash string
        """
        import hashlib

        img = Image.open(image_path)
        # Resize to small size for hash
        img = img.resize((8, 8), Image.Resampling.LANCZOS).convert("L")
        
        # Get average pixel value
        pixels = list(img.getdata())
        avg = sum(pixels) / len(pixels)

        # Create hash based on pixels vs average
        bits = "".join("1" if pixel > avg else "0" for pixel in pixels)
        
        # Convert to hex
        hash_int = int(bits, 2)
        return hashlib.md5(str(hash_int).encode()).hexdigest()

    def clear_diffs(self) -> None:
        """Clear all diff images."""
        for diff_file in self.diff_dir.glob("*.png"):
            diff_file.unlink()

    def clear_baselines(self) -> None:
        """Clear all baseline images."""
        for baseline_file in self.baseline_dir.glob("*.png"):
            baseline_file.unlink()
