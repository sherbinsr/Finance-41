import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, CircularProgress, Container, Tabs, Tab, Box, Grid } from '@mui/material';
import NewsService from '../../Service/NewsService';

const dummyEducationalResources = [
  {
    id: 1,
    title: 'Understanding Investment Strategies',
    content: 'Learn the basics of investment strategies and how to implement them in your portfolio.',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ', // Replace with a valid YouTube video URL
    created_at: '2024-10-01T10:00:00Z',
  },
  {
    id: 2,
    title: 'Market Trends 101',
    content: 'A beginner\'s guide to understanding market trends and their impact on investments.',
    videoUrl: 'https://www.youtube.com/embed/oHg5SJYRHA0', // Replace with a valid YouTube video URL
    created_at: '2024-10-05T12:00:00Z',
  },
  {
    id: 3,
    title: 'Financial Literacy for Everyone',
    content: 'Enhance your financial literacy with practical tips and resources for everyday financial management.',
    videoUrl: 'https://www.youtube.com/embed/wZZ7oFKsKzY', // Replace with a valid YouTube video URL
    created_at: '2024-10-10T15:00:00Z',
  },
  {
    id: 4,
    title: 'Top 10 Investment Tips',
    content: 'Discover essential investment tips that can help you grow your wealth.',
    videoUrl: 'https://www.youtube.com/embed/kJQP7kiw5Fk', // Replace with a valid YouTube video URL
    created_at: '2024-10-15T08:00:00Z',
  },
  {
    id: 5,
    title: 'Risk Management in Investing',
    content: 'Understand the principles of risk management and how to apply them to your investment strategy.',
    videoUrl: 'https://www.youtube.com/embed/tgbNymZ7vqY', // Replace with a valid YouTube video URL
    created_at: '2024-10-20T11:00:00Z',
  },
];

const News = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0); 

  useEffect(() => {
    const fetchArticles = async () => {
      setLoading(true);
      try {
        let data;
        if (tabValue === 0) {
          data = await NewsService.getArticles(); // All News
        } else if (tabValue === 1) {
          data = await NewsService.getLatestArticles(); // Latest News
        } else if (tabValue === 2) {
          // Use the dummy educational resources here
          data = dummyEducationalResources;
        }
        setArticles(data);
      } catch (err) {
        setError('Failed to load articles.');
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, [tabValue]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue); 
  };

  if (loading) return (
    <Box 
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh', 
      }}
    >
      <CircularProgress />
    </Box>
  );

  if (error) return <div>{error}</div>;

  return (
    <Container maxWidth="lg">
      <h2 variant="h2" className="text-center fw-bold text-danger" component="div" style={{ marginTop: 40, marginBottom: 20 }}>
        Market News
      </h2>
      
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="news tabs">
          <Tab label="All News" />
          <Tab label="Latest News" />
          <Tab label="Educational Resources" />
        </Tabs>
      </Box>
      
      {articles.length > 0 ? (
        <Grid container spacing={3} style={{ marginTop: 20 }}>
          {articles.map((article) => (
            <Grid item xs={12} sm={6} key={article.id}>
              <Card style={{ padding: 20, backgroundColor: '#f5f5f5' }}>
                <CardContent>
                  <Typography variant="h5" component="div">
                    {article.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" style={{ marginBottom: '10px' }}>
                    {article.content}
                  </Typography>
                  <Typography variant="caption" color="textSecondary">
                    {new Date(article.created_at).toLocaleString()}
                  </Typography>
                  {article.videoUrl && (
                    <iframe 
                      width="100%" 
                      height="200" 
                      src={article.videoUrl} 
                      title={article.title} 
                      frameBorder="0" 
                      allowFullScreen 
                      style={{ marginTop: '10px' }}
                    />
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      ) : (
        <div>No articles found.</div>
      )}
    </Container>
  );
};

export default News;
