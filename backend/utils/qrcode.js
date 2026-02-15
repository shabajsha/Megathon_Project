const QRCode = require('qrcode');

// Generate QR code for ticket
exports.generateQRCode = async (ticketData) => {
  try {
    const qrData = JSON.stringify({
      ticketId: ticketData.ticketId,
      eventId: ticketData.eventId,
      participantId: ticketData.participantId,
      eventName: ticketData.eventName,
    });
    
    // Generate QR code as base64 string
    const qrCode = await QRCode.toDataURL(qrData);
    return qrCode;
  } catch (error) {
    console.error('QR Code generation failed:', error);
    return null;
  }
};

// Generate unique ticket ID
exports.generateTicketId = () => {
  const timestamp = Date.now().toString(36);
  const randomStr = Math.random().toString(36).substr(2, 5);
  return `TKT-${timestamp}-${randomStr}`.toUpperCase();
};
