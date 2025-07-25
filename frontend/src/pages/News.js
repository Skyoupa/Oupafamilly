import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';

const News = () => {
  const { API_BASE_URL } = useAuth();
  const [newsItems, setNewsItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/content/news`);
      
      if (response.ok) {
        const data = await response.json();
        setNewsItems(data);
      } else {
        setError('Erreur lors du chargement des actualités');
      }
    } catch (error) {
      console.error('Erreur fetch news:', error);
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getNewsTypeIcon = (type) => {
    switch (type) {
      case 'tournament': return '🏆';
      case 'update': return '🔄';
      case 'announcement': return '📢';
      case 'maintenance': return '🔧';
      default: return '📰';
    }
  };

  const getNewsTypeColor = (type) => {
    switch (type) {
      case 'tournament': return 'type-tournament';
      case 'update': return 'type-update';
      case 'announcement': return 'type-announcement';
      case 'maintenance': return 'type-maintenance';
      default: return 'type-default';
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Chargement des actualités...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="error-container">
          <h2>Erreur</h2>
          <p>{error}</p>
          <Link to="/" className="btn-primary">
            Retour à l'accueil
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      {/* Header */}
      <div className="news-header">
        <div className="header-content">
          <div className="news-badge">
            <svg className="news-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M4 6H2V20C2 21.11 2.89 22 4 22H18V20H4V6M20 2H8C6.89 2 6 2.89 6 4V16C6 17.11 6.89 18 8 18H20C21.11 18 22 17.11 22 16V4C22 2.89 21.11 2 20 2M20 16H8V4H20V16M18 14H10V12H18V14M18 11H10V9H18V11M18 8H10V6H18V8Z"/>
            </svg>
            <span>ACTUALITÉS</span>
          </div>
          <h1 className="page-title">Actualités Oupafamilly</h1>
          <p className="page-subtitle">
            Restez informé des dernières nouvelles, mises à jour et événements de la communauté
          </p>
        </div>
      </div>

      {/* News Content */}
      <div className="news-content">
        <div className="container">
          {newsItems.length === 0 ? (
            <div className="no-news">
              <div className="no-news-icon">📰</div>
              <h3>Aucune actualité pour le moment</h3>
              <p>Les actualités de la communauté apparaîtront ici dès qu'elles seront publiées.</p>
            </div>
          ) : (
            <div className="news-grid">
              {newsItems.map(news => (
                <article key={news.id} className="news-card">
                  <div className="news-card-header">
                    <div className={`news-type ${getNewsTypeColor(news.type)}`}>
                      <span className="type-icon">{getNewsTypeIcon(news.type)}</span>
                      <span className="type-label">{news.type}</span>
                    </div>
                    <div className="news-date">
                      {formatDate(news.created_at)}
                    </div>
                  </div>

                  <div className="news-card-content">
                    <h2 className="news-title">{news.title}</h2>
                    <p className="news-excerpt">{news.excerpt}</p>
                    
                    {news.content && (
                      <div className="news-full-content">
                        <div 
                          className="content-text"
                          dangerouslySetInnerHTML={{ 
                            __html: news.content.replace(/\n/g, '<br>')
                          }}
                        />
                      </div>
                    )}

                    {news.image_url && (
                      <div className="news-image">
                        <img 
                          src={news.image_url} 
                          alt={news.title}
                          onError={(e) => {
                            e.target.style.display = 'none';
                          }}
                        />
                      </div>
                    )}
                  </div>

                  <div className="news-card-footer">
                    <div className="news-author">
                      <span className="author-icon">👤</span>
                      <span>Par {news.author_name || 'Équipe Oupafamilly'}</span>
                    </div>
                    
                    {news.tags && news.tags.length > 0 && (
                      <div className="news-tags">
                        {news.tags.map(tag => (
                          <span key={tag} className="news-tag">#{tag}</span>
                        ))}
                      </div>
                    )}
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .page-container {
          min-height: 100vh;
          background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
          color: white;
        }

        .news-header {
          background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
          padding: 3rem 0;
          text-align: center;
        }

        .header-content {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 1rem;
        }

        .news-badge {
          display: inline-flex;
          align-items: center;
          gap: 0.75rem;
          background: rgba(255, 255, 255, 0.2);
          padding: 0.75rem 1.5rem;
          border-radius: 50px;
          font-weight: 600;
          font-size: 0.9rem;
          letter-spacing: 0.5px;
          margin-bottom: 1.5rem;
        }

        .news-icon {
          width: 24px;
          height: 24px;
        }

        .page-title {
          font-size: 3rem;
          font-weight: 700;
          margin: 0 0 1rem 0;
          text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .page-subtitle {
          font-size: 1.2rem;
          opacity: 0.9;
          max-width: 600px;
          margin: 0 auto;
          line-height: 1.6;
        }

        .news-content {
          padding: 3rem 0;
        }

        .container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 1rem;
        }

        .no-news {
          text-align: center;
          padding: 4rem 2rem;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 16px;
          border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .no-news-icon {
          font-size: 4rem;
          margin-bottom: 1rem;
        }

        .no-news h3 {
          color: #e2e8f0;
          font-size: 1.5rem;
          margin: 0 0 1rem 0;
        }

        .no-news p {
          color: #94a3b8;
          font-size: 1.1rem;
          margin: 0;
        }

        .news-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
          gap: 2rem;
        }

        .news-card {
          background: rgba(255, 255, 255, 0.05);
          border-radius: 16px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          overflow: hidden;
          transition: all 0.3s ease;
          backdrop-filter: blur(10px);
        }

        .news-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
          border-color: rgba(59, 130, 246, 0.3);
        }

        .news-card-header {
          padding: 1.5rem 1.5rem 0 1.5rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }

        .news-type {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-size: 0.8rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .type-tournament { background: rgba(251, 191, 36, 0.2); color: #fbbf24; }
        .type-update { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
        .type-announcement { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
        .type-maintenance { background: rgba(156, 163, 175, 0.2); color: #9ca3af; }
        .type-default { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }

        .type-icon {
          font-size: 1rem;
        }

        .news-date {
          color: #94a3b8;
          font-size: 0.85rem;
          font-weight: 500;
        }

        .news-card-content {
          padding: 0 1.5rem 1.5rem 1.5rem;
        }

        .news-title {
          color: #e2e8f0;
          font-size: 1.4rem;
          font-weight: 600;
          margin: 0 0 1rem 0;
          line-height: 1.4;
        }

        .news-excerpt {
          color: #cbd5e1;
          font-size: 1rem;
          line-height: 1.6;
          margin: 0 0 1.5rem 0;
        }

        .news-full-content {
          margin-bottom: 1.5rem;
        }

        .content-text {
          color: #e2e8f0;
          font-size: 0.95rem;
          line-height: 1.7;
          background: rgba(255, 255, 255, 0.02);
          padding: 1rem;
          border-radius: 8px;
          border-left: 3px solid #3b82f6;
        }

        .news-image {
          margin: 1.5rem 0;
          border-radius: 8px;
          overflow: hidden;
        }

        .news-image img {
          width: 100%;
          height: 200px;
          object-fit: cover;
          transition: transform 0.3s ease;
        }

        .news-card:hover .news-image img {
          transform: scale(1.05);
        }

        .news-card-footer {
          padding: 1rem 1.5rem;
          border-top: 1px solid rgba(255, 255, 255, 0.1);
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 1rem;
        }

        .news-author {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: #94a3b8;
          font-size: 0.9rem;
        }

        .author-icon {
          font-size: 1rem;
        }

        .news-tags {
          display: flex;
          gap: 0.5rem;
          flex-wrap: wrap;
        }

        .news-tag {
          background: rgba(59, 130, 246, 0.2);
          color: #93c5fd;
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .loading-container,
        .error-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          min-height: 50vh;
          padding: 2rem;
          text-align: center;
        }

        .loading-spinner {
          width: 40px;
          height: 40px;
          border: 4px solid rgba(255, 255, 255, 0.3);
          border-left: 4px solid #3b82f6;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 1rem;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .btn-primary {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 600;
          display: inline-flex;
          align-items: center;
          transition: all 0.3s;
        }

        .btn-primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
        }

        /* Responsive Design */
        @media (max-width: 768px) {
          .page-title {
            font-size: 2rem;
          }

          .page-subtitle {
            font-size: 1rem;
          }

          .news-grid {
            grid-template-columns: 1fr;
          }

          .news-card-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
          }

          .news-card-footer {
            flex-direction: column;
            align-items: flex-start;
          }

          .header-content {
            padding: 0 1rem;
          }

          .news-header {
            padding: 2rem 0;
          }
        }
      `}</style>
    </div>
  );
};

export default News;