import nodemailer from "nodemailer";

export default async function handler(req, res) {
  const { email, subject, message } = req.query;

  if (!email || !subject || !message) {
    return res.status(400).json({ success: false, error: "Missing parameters" });
  }

  let transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: process.env.GMAIL_USER,
      pass: process.env.GMAIL_PASS,
    },
  });

  try {
    await transporter.sendMail({
      from: `"Test Bot" <${process.env.GMAIL_USER}>`,
      to: email,
      subject: subject,
      text: message,
    });
    res.json({ success: true, message: "Email sent" });
  } catch (e) {
    res.status(500).json({ success: false, error: e.message });
  }
        }
