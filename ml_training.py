"""
ML Training Module - For Car Damage Detection
This file is for your friend who is doing the machine learning training
"""

import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image
import numpy as np

class CarDamageModel:
    """Car damage detection model wrapper for easy integration."""
    
    def __init__(self, model_path=None, model_type="severity"):
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.transform = self.get_transform()
        self.model_type = model_type
        
        if model_type == "severity":
            self.class_names = ['low', 'moderate', 'heavy']
            self.num_classes = 3
        elif model_type == "damage_type":
            self.class_names = ['scratch', 'dent', 'crack', 'paint_damage', 'bumper_damage', 'glass_damage']
            self.num_classes = 6
        
        if model_path:
            self.load_model(model_path)
    
    def get_transform(self):
        """Get image transformation pipeline."""
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    
    def load_model(self, model_path):
        """Load trained model from file."""
        try:
            # First, try to load the state dict to check the architecture
            state_dict = torch.load(model_path, map_location=self.device)
            
            # Check if this is a ResNet50 model (based on fc layer size)
            if 'fc.weight' in state_dict:
                fc_weight_shape = state_dict['fc.weight'].shape
                if fc_weight_shape[1] == 2048:  # ResNet50
                    from torchvision.models import resnet50, ResNet50_Weights
                    weights = ResNet50_Weights.DEFAULT
                    self.model = resnet50(weights=weights)
                    self.model.fc = nn.Linear(self.model.fc.in_features, fc_weight_shape[0])
                else:  # ResNet18
                    weights = ResNet18_Weights.DEFAULT
                    self.model = resnet18(weights=weights)
                    self.model.fc = nn.Linear(self.model.fc.in_features, fc_weight_shape[0])
            else:
                # Default to ResNet18
                weights = ResNet18_Weights.DEFAULT
                self.model = resnet18(weights=weights)
                self.model.fc = nn.Linear(self.model.fc.in_features, self.num_classes)
            
            # Load trained weights
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            return True
        except Exception as e:
            print(f"Error loading {self.model_type} model: {e}")
            return False
    
    def predict_damage(self, image):
        """Predict damage from image (severity or type)."""
        if self.model is None:
            return self.get_placeholder_prediction(image)
        
        try:
            # Preprocess image
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)
            
            # Get the actual number of classes from the model
            num_classes = outputs.shape[1]
            predicted_idx = predicted_class.item()
            
            # Map prediction to class name
            if self.model_type == "severity":
                if num_classes == 3:
                    class_names = ['low', 'moderate', 'heavy']
                elif num_classes == 8:
                    # Map 8 classes to 3 severity levels
                    class_names = ['low', 'moderate', 'heavy', 'low', 'moderate', 'heavy', 'low', 'moderate']
                else:
                    class_names = ['low', 'moderate', 'heavy'][:num_classes]
                prediction = class_names[predicted_idx] if predicted_idx < len(class_names) else 'moderate'
            else:  # damage_type
                if num_classes == 6:
                    class_names = ['scratch', 'dent', 'crack', 'paint_damage', 'bumper_damage', 'glass_damage']
                else:
                    class_names = ['scratch', 'dent', 'crack', 'paint_damage', 'bumper_damage', 'glass_damage'][:num_classes]
                prediction = class_names[predicted_idx] if predicted_idx < len(class_names) else 'scratch'
            
            confidence_score = confidence.item()
            
            if self.model_type == "severity":
                return {
                    "severity": prediction,
                    "confidence": confidence_score,
                    "all_probabilities": probabilities[0].cpu().numpy().tolist(),
                    "model_used": True
                }
            else:  # damage_type
                return {
                    "damage_type": prediction,
                    "confidence": confidence_score,
                    "all_probabilities": probabilities[0].cpu().numpy().tolist(),
                    "model_used": True
                }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return self.get_placeholder_prediction(image)
    
    def get_placeholder_prediction(self, image):
        """Placeholder prediction when model is not available."""
        import random
        
        # Generate consistent results based on image
        image_hash = hash(str(image.size) + str(image.mode))
        random.seed(image_hash)
        
        prediction = random.choice(self.class_names)
        confidence = random.uniform(0.7, 0.95)
        
        if self.model_type == "severity":
            return {
                "severity": prediction,
                "confidence": confidence,
                "all_probabilities": [0.3, 0.4, 0.3],  # Placeholder
                "model_used": False
            }
        else:  # damage_type
            return {
                "damage_type": prediction,
                "confidence": confidence,
                "all_probabilities": [0.2, 0.2, 0.2, 0.2, 0.1, 0.1],  # Placeholder
                "model_used": False
            }

# Global model instances
severity_model = CarDamageModel(model_type="severity")
damage_type_model = CarDamageModel(model_type="damage_type")

def initialize_models():
    """Initialize both damage detection models."""
    global severity_model, damage_type_model
    
    # Try to load severity model
    severity_paths = ["data3a/car_damage_model.pth", "car_damage_model.pth", "data3a/car_severity_model.pth"]
    severity_loaded = False
    for path in severity_paths:
        if severity_model.load_model(path):
            severity_loaded = True
            break
    
    # Try to load damage type model
    damage_type_paths = ["data3a/car_damage_type_model.pth", "car_damage_type_model.pth", "damage_type_model.pth"]
    damage_type_loaded = False
    for path in damage_type_paths:
        if damage_type_model.load_model(path):
            damage_type_loaded = True
            break
    
    return severity_loaded, damage_type_loaded

def predict_car_damage_severity(image):
    """Predict car damage severity - call this from app.py"""
    return severity_model.predict_damage(image)

def predict_car_damage_type(image):
    """Predict car damage type - call this from app.py"""
    return damage_type_model.predict_damage(image)

def predict_car_damage_complete(image):
    """Predict both severity and damage type - call this from app.py"""
    severity_result = predict_car_damage_severity(image)
    damage_type_result = predict_car_damage_type(image)
    
    # Combine results
    combined_result = {
        "severity": severity_result.get("severity", "unknown"),
        "damage_type": damage_type_result.get("damage_type", "unknown"),
        "severity_confidence": severity_result.get("confidence", 0.0),
        "damage_type_confidence": damage_type_result.get("confidence", 0.0),
        "severity_model_used": severity_result.get("model_used", False),
        "damage_type_model_used": damage_type_result.get("model_used", False)
    }
    
    return combined_result
