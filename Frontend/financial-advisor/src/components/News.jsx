import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, CircularProgress, Container } from '@mui/material';
import NewsService from '../Service/NewsService'; 

const News = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const data = await NewsService.getArticles(); 
        setArticles(data);
        console.log(data);
      } catch (err) {
        setError('Failed to load articles.');
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, []);

  if (loading) return <CircularProgress />;
  if (error) return <div>{error}</div>;

  return (
    <Container maxWidth="sm">
      {articles.length > 0 ? (
        articles.map((article) => (
          <Card key={article.id} style={{ marginTop: 20, padding: 20, backgroundColor: '#f5f5f5' }}>
            <CardContent>
              <Typography variant="h5" component="div">
                {article.title}
              </Typography>
              <Typography variant="body2" color="text.secondary" style={{ marginBottom: '10px' }}>
                {article.content}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                {new Date(article.created_at).toLocaleString()}  {/* Display formatted date */}
              </Typography>
            </CardContent>
          </Card>
        ))
      ) : (
        <div>No articles found.</div>
      )}
    </Container>
  );
};

export default News;
