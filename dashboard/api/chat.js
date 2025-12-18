// Vercel Serverless Function for Gemini Chat
// Uses gemini-3-flash-preview for fast responses

export default async function handler(req, res) {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { message, context } = req.body;

    if (!message) {
        return res.status(400).json({ error: 'Message is required' });
    }

    const apiKey = process.env.GEMINI_API_KEY;

    if (!apiKey) {
        console.error('GEMINI_API_KEY not configured');
        return res.status(500).json({ error: 'API key not configured' });
    }

    try {
        const response = await fetch(
            `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${apiKey}`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{
                        parts: [{
                            text: `${context}\n\nUser question: ${message}`
                        }]
                    }],
                    generationConfig: {
                        maxOutputTokens: 1024,
                        temperature: 0.7
                    }
                })
            }
        );

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Gemini API error:', errorText);
            throw new Error('Gemini API error');
        }

        const data = await response.json();
        const aiResponse = data.candidates?.[0]?.content?.parts?.[0]?.text ||
            "I'm having trouble responding right now. Please try again!";

        return res.status(200).json({ response: aiResponse });

    } catch (error) {
        console.error('Chat API error:', error);
        return res.status(500).json({
            error: 'Failed to get response',
            response: "Sorry, I'm having trouble connecting. Please try again in a moment!"
        });
    }
}
