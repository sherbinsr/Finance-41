import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, CircularProgress, Container, Tabs, Tab, Box, Grid } from '@mui/material';
import NewsService from '../../Service/NewsService';

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
          data = await NewsService.getArticles();
        } else if (tabValue === 1) {
          data = await NewsService.getLatestArticles(); 
        } else if (tabValue === 2) {
          data = await NewsService.getEducationalResources();
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
                  {article.video_url && (
                 <iframe 
                  width="100%" 
                  height="200" 
                  src={article.video_url.replace('watch?v=', 'embed/')} 
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
