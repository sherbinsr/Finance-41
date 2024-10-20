import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, CircularProgress, Container, Tabs, Tab, Box, Grid } from '@mui/material';
import NewsService from '../Service/NewsService'; 

const News = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0); 

  useEffect(() => {
    const fetchArticles = async () => {
      setLoading(true);
      try {
        const data = tabValue === 0
          ? await NewsService.getArticles()      
          : await NewsService.getLatestArticles(); 

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

  if (loading) return <CircularProgress />;
  if (error) return <div>{error}</div>;

  return (
    <Container maxWidth="lg">
      <h2 variant="h2" class="text-center fw-bold text-danger"  component="div" style={{ marginTop: 40, marginBottom: 20 }}>
        Market News
      </h2>
      
      <Box  sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs  value={tabValue} onChange={handleTabChange} aria-label="news tabs">
          <Tab label="All News" />
          <Tab label="Latest News" />
        </Tabs>
      </Box>
      
      {articles.length > 0 ? (
        <Grid container spacing={3} style={{ marginTop: 20 }}> {/* Grid container with spacing */}
          {articles.map((article) => (
            <Grid item xs={12} sm={6} key={article.id}> {/* xs=12 for full width on small screens, sm=6 for two columns */}
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
