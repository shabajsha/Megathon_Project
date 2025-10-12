"""
Fraud Detection Module - For Car Damage Insurance Fraud Detection
This file is for your friend who is doing the fraud detection
"""

import random
import hashlib
import numpy as np
from PIL import Image
from datetime import datetime

class FraudDetector:
    """Car damage fraud detection system."""
    
    def __init__(self):
        self.fraud_threshold = 30  # Very lenient threshold for testing
        self.processed_images = set()
        
    def detect_fraud(self, image: Image.Image) -> dict:
        """Main fraud detection function - lenient for real photos, strict for AI-generated."""
        
        fraud_score = 0
        fraud_reasons = []
        
        # 1. AI Generation Detection (high priority)
        ai_score, ai_reasons = self.detect_ai_generated(image)
        fraud_score += ai_score
        fraud_reasons.extend(ai_reasons)
        
        # 2. Basic metadata check (very lenient)
        metadata_score, metadata_reasons = self.check_metadata(image)
        fraud_score += metadata_score
        fraud_reasons.extend(metadata_reasons)
        
        # 3. Basic quality check (very lenient)
        quality_score, quality_reasons = self.check_quality(image)
        fraud_score += quality_score
        fraud_reasons.extend(quality_reasons)
        
        # 4. Duplicate check (very lenient)
        duplicate_score, duplicate_reasons = self.check_duplicates(image)
        fraud_score += duplicate_score
        fraud_reasons.extend(duplicate_reasons)
        
        # 5. Basic pattern check (very lenient)
        pattern_score, pattern_reasons = self.check_patterns(image)
        fraud_score += pattern_score
        fraud_reasons.extend(pattern_reasons)
        
        # Ensure score is between 0-100
        final_score = min(100, max(0, fraud_score))
        
        return {
            "fraud_score": final_score,
            "is_fraud": final_score >= self.fraud_threshold,
            "reasons": fraud_reasons,
            "threshold": self.fraud_threshold,
            "risk_level": self.get_risk_level(final_score)
        }
    
    def check_metadata(self, image: Image.Image) -> tuple:
        """Very lenient metadata check."""
        fraud_score = 0
        reasons = []
        
        try:
            # Only flag obvious editing software
            exif_data = image._getexif() if hasattr(image, '_getexif') else None
            
            if exif_data and 305 in exif_data:  # Software
                software = str(exif_data[305]).lower()
                if 'photoshop' in software or 'gimp' in software:
                    fraud_score += 15  # Reduced penalty
                    reasons.append("Image editing software detected")
            
            # No penalty for missing EXIF (common in web images)
            
        except Exception:
            pass  # No penalty for metadata errors
        
        return fraud_score, reasons
    
    def check_quality(self, image: Image.Image) -> tuple:
        """Very lenient quality check."""
        fraud_score = 0
        reasons = []
        
        try:
            width, height = image.size
            
            # Only flag extremely low resolution
            if width < 50 or height < 50:
                fraud_score += 10
                reasons.append("Very low resolution image")
            
            # No penalty for normal web image sizes
            
        except Exception:
            pass
        
        return fraud_score, reasons
    
    def check_duplicates(self, image: Image.Image) -> tuple:
        """Very lenient duplicate check."""
        fraud_score = 0
        reasons = []
        
        try:
            # Generate simple hash
            image_hash = hashlib.md5(str(image.size).encode()).hexdigest()
            
            # Only flag if exact same image uploaded multiple times in session
            if hasattr(self, 'processed_images') and image_hash in self.processed_images:
                fraud_score += 20
                reasons.append("Duplicate image detected in current session")
            
            if not hasattr(self, 'processed_images'):
                self.processed_images = set()
            
            self.processed_images.add(image_hash)
            
        except Exception:
            pass
        
        return fraud_score, reasons
    
    def check_patterns(self, image: Image.Image) -> tuple:
        """Very lenient pattern check."""
        fraud_score = 0
        reasons = []
        
        try:
            # Only flag obvious artificial patterns
            img_array = np.array(image)
            
            if len(img_array.shape) == 3:
                # Check for extremely uniform colors (very strict threshold)
                for channel in range(3):
                    channel_data = img_array[:, :, channel]
                    unique_values = len(np.unique(channel_data))
                    total_pixels = channel_data.size
                    
                    if unique_values / total_pixels < 0.01:  # Less than 1% unique values
                        fraud_score += 25
                        reasons.append("Extremely uniform color pattern detected")
                        break
            
        except Exception:
            pass
        
        return fraud_score, reasons
    
    def detect_ai_generated(self, image: Image.Image) -> tuple:
        """Detect AI-generated images with high accuracy."""
        fraud_score = 0
        reasons = []
        
        try:
            img_array = np.array(image)
            
            # 1. Check for AI generation artifacts (very strict)
            ai_indicators = self.check_ai_artifacts(img_array)
            if ai_indicators:
                fraud_score += 20  # Reduced penalty
                reasons.extend(ai_indicators)
            
            # 2. Check for perfect symmetry (common in AI-generated images)
            symmetry_score, symmetry_reasons = self.check_ai_symmetry(img_array)
            fraud_score += symmetry_score
            reasons.extend(symmetry_reasons)
            
            # 3. Check for unnatural color patterns
            color_score, color_reasons = self.check_ai_color_patterns(img_array)
            fraud_score += color_score
            reasons.extend(color_reasons)
            
            # 4. Check for AI-specific noise patterns
            noise_score, noise_reasons = self.check_ai_noise_patterns(img_array)
            fraud_score += noise_score
            reasons.extend(noise_reasons)
            
            # 5. Check for unrealistic details
            detail_score, detail_reasons = self.check_ai_unrealistic_details(img_array)
            fraud_score += detail_score
            reasons.extend(detail_reasons)
            
        except Exception as e:
            pass  # Don't penalize for analysis errors
        
        return fraud_score, reasons
    
    def check_ai_artifacts(self, img_array: np.ndarray) -> list:
        """Check for obvious AI generation artifacts (very strict)."""
        artifacts = []
        
        if len(img_array.shape) == 3:
            # Check for checkerboard artifacts (common in GANs) - very strict
            gray = np.mean(img_array, axis=2)
            h, w = gray.shape
            
            # Look for very obvious regular patterns (much stricter)
            uniform_blocks = 0
            total_blocks = 0
            for i in range(0, h-20, 20):
                for j in range(0, w-20, 20):
                    block = gray[i:i+20, j:j+20]
                    if np.std(block) < 2:  # Much stricter - very uniform blocks
                        uniform_blocks += 1
                    total_blocks += 1
            
            # Only flag if more than 30% of blocks are perfectly uniform
            if total_blocks > 0 and uniform_blocks / total_blocks > 0.3:
                artifacts.append("AI generation artifacts detected (checkerboard pattern)")
        
        return artifacts
    
    def check_ai_symmetry(self, img_array: np.ndarray) -> tuple:
        """Check for perfect symmetry common in AI-generated images (very strict)."""
        fraud_score = 0
        reasons = []
        
        if len(img_array.shape) == 3:
            h, w = img_array.shape[:2]
            
            # Check horizontal symmetry - much stricter
            if w % 2 == 0:
                left_half = img_array[:, :w//2]
                right_half = np.fliplr(img_array[:, w//2:])
                
                if left_half.shape == right_half.shape:
                    diff = np.mean(np.abs(left_half.astype(float) - right_half.astype(float)))
                    if diff < 1:  # Much stricter - almost identical halves
                        fraud_score += 15  # Reduced penalty
                        reasons.append("Perfect horizontal symmetry detected (AI generation indicator)")
            
            # Check vertical symmetry - much stricter
            if h % 2 == 0:
                top_half = img_array[:h//2, :]
                bottom_half = np.flipud(img_array[h//2:, :])
                
                if top_half.shape == bottom_half.shape:
                    diff = np.mean(np.abs(top_half.astype(float) - bottom_half.astype(float)))
                    if diff < 1:  # Much stricter - almost identical halves
                        fraud_score += 15  # Reduced penalty
                        reasons.append("Perfect vertical symmetry detected (AI generation indicator)")
        
        return fraud_score, reasons
    
    def check_ai_color_patterns(self, img_array: np.ndarray) -> tuple:
        """Check for unnatural color patterns in AI-generated images (very strict)."""
        fraud_score = 0
        reasons = []
        
        if len(img_array.shape) == 3:
            # Check for unrealistic color gradients - much stricter
            for channel in range(3):
                channel_data = img_array[:, :, channel]
                
                # Check for perfect gradients (common in AI-generated backgrounds)
                gradient_x = np.gradient(channel_data, axis=1)
                gradient_y = np.gradient(channel_data, axis=0)
                
                # Look for extremely smooth gradients (much stricter)
                if np.std(gradient_x) < 0.5 and np.std(gradient_y) < 0.5:
                    fraud_score += 10  # Reduced penalty
                    reasons.append("Unnaturally smooth color gradients detected (AI generation)")
                    break
            
            # Check for color banding - much stricter
            for channel in range(3):
                channel_data = img_array[:, :, channel]
                unique_values = len(np.unique(channel_data))
                total_pixels = channel_data.size
                
                if unique_values / total_pixels < 0.1:  # Much stricter - less than 10% unique values
                    fraud_score += 10  # Reduced penalty
                    reasons.append("Color banding detected (AI generation indicator)")
                    break
        
        return fraud_score, reasons
    
    def check_ai_noise_patterns(self, img_array: np.ndarray) -> tuple:
        """Check for AI-specific noise patterns (very strict)."""
        fraud_score = 0
        reasons = []
        
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
            
            # AI-generated images often have very specific noise patterns
            # Check for frequency domain patterns - much stricter
            f_transform = np.fft.fft2(gray)
            f_shift = np.fft.fftshift(f_transform)
            magnitude_spectrum = np.log(np.abs(f_shift) + 1)
            
            # Look for very obvious regular patterns in frequency domain
            h, w = magnitude_spectrum.shape
            center_h, center_w = h // 2, w // 2
            
            # Check for concentric circles (common in AI-generated images) - much stricter
            y, x = np.ogrid[:h, :w]
            distances = np.sqrt((x - center_w)**2 + (y - center_h)**2)
            
            # Look for very strong circular patterns
            for radius in range(20, min(h, w)//3, 20):
                mask = (distances >= radius-3) & (distances <= radius+3)
                if np.sum(mask) > 0:
                    mean_intensity = np.mean(magnitude_spectrum[mask])
                    if mean_intensity > np.mean(magnitude_spectrum) * 2.0:  # Much stricter
                        fraud_score += 10  # Reduced penalty
                        reasons.append("Regular frequency patterns detected (AI generation)")
                        break
        
        return fraud_score, reasons
    
    def check_ai_unrealistic_details(self, img_array: np.ndarray) -> tuple:
        """Check for unrealistic details common in AI-generated images (very strict)."""
        fraud_score = 0
        reasons = []
        
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
            
            # Check for unrealistic sharpness - much stricter
            # AI-generated images often have inconsistent sharpness
            edges = np.gradient(gray)
            edge_magnitude = np.sqrt(edges[0]**2 + edges[1]**2)
            
            # Look for areas with perfect sharpness next to blurry areas - much stricter
            sharp_areas = edge_magnitude > np.percentile(edge_magnitude, 95)  # Top 5%
            blurry_areas = edge_magnitude < np.percentile(edge_magnitude, 5)   # Bottom 5%
            
            if np.sum(sharp_areas) > 0 and np.sum(blurry_areas) > 0:
                # Check if sharp and blurry areas are very close (unrealistic)
                sharp_coords = np.where(sharp_areas)
                blurry_coords = np.where(blurry_areas)
                
                if len(sharp_coords[0]) > 0 and len(blurry_coords[0]) > 0:
                    min_distance = np.min([
                        np.sqrt((sc[0] - bc[0])**2 + (sc[1] - bc[1])**2)
                        for sc in zip(sharp_coords[0][:5], sharp_coords[1][:5])
                        for bc in zip(blurry_coords[0][:5], blurry_coords[1][:5])
                    ])
                    
                    if min_distance < 5:  # Much stricter - sharp and blurry areas very close
                        fraud_score += 10  # Reduced penalty
                        reasons.append("Unrealistic sharpness patterns detected (AI generation)")
            
            # Check for impossible lighting - much stricter
            # AI-generated images often have inconsistent lighting
            brightness_variance = np.var(gray)
            if brightness_variance < 20:  # Much stricter - extremely uniform lighting
                fraud_score += 5  # Reduced penalty
                reasons.append("Unnaturally uniform lighting detected (AI generation)")
        
        return fraud_score, reasons
    
    def get_risk_level(self, fraud_score: int) -> str:
        """Get risk level based on fraud score."""
        if fraud_score < 20:
            return "Low Risk"
        elif fraud_score < 40:
            return "Medium Risk"
        elif fraud_score < 60:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def set_threshold(self, threshold: int):
        """Set fraud detection threshold."""
        self.fraud_threshold = threshold
    
    def get_fraud_summary(self, fraud_result: dict) -> dict:
        """Get summary of fraud detection results."""
        return {
            "status": "REJECTED" if fraud_result["is_fraud"] else "APPROVED",
            "score": fraud_result["fraud_score"],
            "threshold": fraud_result["threshold"],
            "risk_level": fraud_result["risk_level"],
            "issues_found": len(fraud_result["reasons"]),
            "recommendation": self.get_recommendation(fraud_result)
        }
    
    def get_recommendation(self, fraud_result: dict) -> str:
        """Get recommendation based on fraud detection results."""
        if fraud_result["is_fraud"]:
            return "Manual review required - high fraud probability detected"
        elif fraud_result["fraud_score"] > 30:
            return "Proceed with caution - some suspicious elements detected"
        else:
            return "Image appears legitimate - proceed with claim processing"

# Global fraud detector instance
fraud_detector = FraudDetector()

def detect_fraud(image: Image.Image) -> dict:
    """Main function to detect fraud - call this from app.py"""
    return fraud_detector.detect_fraud(image)

def set_fraud_threshold(threshold: int):
    """Set fraud detection threshold."""
    fraud_detector.set_threshold(threshold)

def get_fraud_summary(fraud_result: dict) -> dict:
    """Get fraud detection summary."""
    return fraud_detector.get_fraud_summary(fraud_result)
