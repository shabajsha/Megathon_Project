# 🚗 Car Damage Assessment AI

A comprehensive Streamlit web application that uses artificial intelligence to analyze car damage from uploaded images. The app provides detailed damage assessment including severity, type, cost estimation, and fraud detection with visual explanations.

## ✨ Features

### 🔍 Damage Analysis
- **Damage Type Detection**: Identifies specific types of damage (scratch, dent, broken glass, etc.)
- **Severity Assessment**: Classifies damage as minor, moderate, or severe
- **Cost Estimation**: Provides approximate repair cost ranges
- **Confidence Scoring**: Shows model confidence in predictions

### 🛡️ Security Features
- **Fraud Detection**: Flags potential tampering or fraudulent images
- **Adjustable Thresholds**: Customizable fraud detection sensitivity
- **Alert System**: Clear warnings when fraud is detected

### 🎯 Visual Explanations
- **Grad-CAM Heatmaps**: Shows which parts of the image the AI focuses on
- **Interactive Overlays**: Adjustable opacity for better visualization
- **Real-time Analysis**: Instant results with visual feedback

### 🎨 User Experience
- **Modern UI**: Clean, professional interface with custom styling
- **Responsive Design**: Works on different screen sizes
- **Interactive Controls**: Adjustable settings in sidebar
- **Detailed Reports**: Expandable sections for comprehensive analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd car-damage-assessment
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL manually

## 📖 How to Use

### 1. Upload an Image
- Use the sidebar to upload a car image (PNG, JPG, or JPEG)
- Ensure the image is clear and shows the damage area

### 2. Review Analysis
- The app will display the original image alongside a Grad-CAM heatmap
- Review the damage assessment results in the metrics section

### 3. Check for Fraud
- Pay attention to fraud detection alerts
- Adjust the fraud threshold in the sidebar if needed

### 4. Explore Details
- Use the expandable sections to see detailed analysis
- Learn about Grad-CAM visualization in the help section

## 🔧 Configuration

### Adjustable Settings
- **Grad-CAM Overlay Opacity**: Control heatmap transparency (0.1 - 0.8)
- **Fraud Detection Threshold**: Set sensitivity for fraud detection (0.1 - 0.9)

### Supported Image Formats
- PNG
- JPG/JPEG
- Maximum file size: 200MB (Streamlit default)

## 🏗️ Technical Details

### Architecture
- **Frontend**: Streamlit web framework
- **Image Processing**: OpenCV and PIL
- **Visualization**: Matplotlib with custom colormaps
- **Mock AI**: Simulated prediction models for demonstration

### Key Components
- `CarDamagePredictor`: Mock AI model for damage assessment
- `generate_gradcam()`: Creates attention heatmaps
- `create_gradcam_overlay()`: Blends heatmaps with original images
- Custom CSS styling for professional appearance

### Mock Predictions
The current implementation uses mock predictions that simulate:
- 7 different damage types
- 3 severity levels
- Cost bands based on severity
- Fraud probability scoring
- Confidence metrics

## 🔮 Future Enhancements

### Real AI Integration
- Replace mock models with actual trained neural networks
- Implement real Grad-CAM from deep learning models
- Add support for multiple car makes and models

### Additional Features
- Batch processing for multiple images
- Export reports to PDF
- Integration with insurance databases
- Mobile app version
- API endpoints for external integration

### Performance Improvements
- GPU acceleration for faster processing
- Image preprocessing optimization
- Caching for repeated analyses
- Asynchronous processing

## 🛠️ Development

### Project Structure
```
car-damage-assessment/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Adding Real AI Models
To integrate actual AI models:

1. **Replace the mock predictor** in `CarDamagePredictor.predict_damage()`
2. **Implement real Grad-CAM** in `generate_gradcam()`
3. **Add model loading** and preprocessing functions
4. **Update requirements.txt** with ML framework dependencies

### Customization
- Modify damage types in `self.damage_types`
- Adjust cost bands in `self.cost_bands`
- Customize UI colors in the CSS section
- Add new visualization options

## 📝 License

This project is for demonstration purposes. Please ensure you have appropriate licenses for any production use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📞 Support

For questions or support, please refer to the Streamlit documentation or create an issue in the project repository.

---

**Note**: This is a demonstration application with mock AI models. For production use, integrate with actual trained machine learning models and ensure proper validation and testing.
