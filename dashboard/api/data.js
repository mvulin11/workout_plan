// Vercel serverless function to fetch dashboard data from GitHub
// This avoids CORS and caching issues with raw GitHub URLs

export default async function handler(req, res) {
    try {
        const response = await fetch(
            'https://raw.githubusercontent.com/mvulin11/workout_plan/main/dashboard_data.json',
            { cache: 'no-store' }
        );

        if (!response.ok) {
            throw new Error(`GitHub returned ${response.status}`);
        }

        const data = await response.json();

        // Enable CORS
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');

        return res.status(200).json(data);
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
        return res.status(500).json({
            error: 'Failed to fetch dashboard data',
            message: error.message
        });
    }
}
