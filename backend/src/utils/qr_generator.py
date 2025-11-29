"""
QR Code Generator - Medical Information for First Responders

Generates QR codes containing critical medical information.
"""

import json
import qrcode
from io import BytesIO
from typing import Dict, Any


def generate_medical_qr(medical_data: Dict[str, Any]) -> bytes:
    """
    Generate QR code containing medical information for first responders.
    
    Args:
        medical_data: Dictionary containing:
            - blood_type: str
            - allergies: List[str]
            - emergency_contact: str
            - vitals: dict (optional)
            - incident_id: str (optional)
            
    Returns:
        PNG image bytes of the QR code
    """
    # Create JSON payload
    payload = {
        "blood_type": medical_data.get("blood_type", "Unknown"),
        "allergies": medical_data.get("allergies", []),
        "emergency_contact": medical_data.get("emergency_contact", ""),
        "incident_id": medical_data.get("incident_id", ""),
        "vitals": medical_data.get("vitals", {})
    }
    
    # Convert to JSON string
    json_data = json.dumps(payload, indent=2)
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json_data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()


def generate_first_responder_dashboard_data(medical_data: Dict[str, Any]) -> str:
    """
    Generate HTML/text content for first responder dashboard.
    
    Args:
        medical_data: Medical information dictionary
        
    Returns:
        HTML string for dashboard display
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>First Responder Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }}
            .dashboard {{ background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }}
            h1 {{ color: #d32f2f; }}
            .info-section {{ margin: 20px 0; padding: 15px; background: #f5f5f5; border-radius: 5px; }}
            .label {{ font-weight: bold; color: #666; }}
            .value {{ color: #000; margin-left: 10px; }}
            .qr-code {{ text-align: center; margin: 20px 0; }}
            .alert {{ background: #ffebee; padding: 15px; border-left: 4px solid #d32f2f; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="dashboard">
            <h1>🚨 First Responder Dashboard</h1>
            
            <div class="alert">
                <strong>EMERGENCY MEDICAL INFORMATION</strong>
            </div>
            
            <div class="info-section">
                <div><span class="label">Blood Type:</span><span class="value">{medical_data.get('blood_type', 'Unknown')}</span></div>
            </div>
            
            <div class="info-section">
                <div><span class="label">Allergies:</span></div>
                <div class="value">
                    {', '.join(medical_data.get('allergies', [])) if medical_data.get('allergies') else 'None'}
                </div>
            </div>
            
            <div class="info-section">
                <div><span class="label">Emergency Contact:</span></div>
                <div class="value">{medical_data.get('emergency_contact', 'Not provided')}</div>
            </div>
            
            <div class="info-section">
                <div><span class="label">Incident ID:</span></div>
                <div class="value">{medical_data.get('incident_id', 'Unknown')}</div>
            </div>
            
            <div class="qr-code">
                <p><strong>Scan QR Code for Full Medical Profile</strong></p>
                <p style="font-size: 12px; color: #666;">QR code contains complete medical information in JSON format</p>
            </div>
            
            <div class="alert">
                <strong>⚠️ DO NOT LOCK THIS SCREEN</strong><br>
                This information is critical for emergency responders.
            </div>
        </div>
    </body>
    </html>
    """
    return html

