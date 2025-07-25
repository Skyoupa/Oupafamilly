import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const AdminContent = () => {
  const { user, token, API_BASE_URL } = useAuth();
  const [activeTab, setActiveTab] = useState('news');
  const [news, setNews] = useState([]);
  const [tutorials, setTutorials] = useState([]);
  const [contentStats, setContentStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    summary: '',
    tags: '',
    is_pinned: false,
    game: 'cs2',
    level: 'beginner',
    video_url: ''
  });

  const games = [
    { id: 'cs2', name: 'Counter-Strike 2' },
    { id: 'lol', name: 'League of Legends' },
    { id: 'wow', name: 'World of Warcraft' },
    { id: 'sc2', name: 'StarCraft II' },
    { id: 'minecraft', name: 'Minecraft' }
  ];

  const levels = [
    { id: 'beginner', name: 'Débutant' },
    { id: 'intermediate', name: 'Intermédiaire' },
    { id: 'expert', name: 'Expert' }
  ];

  useEffect(() => {
    if (user?.role === 'admin') {
      fetchContent();
      fetchContentStats();
    }
  }, [user, activeTab]);

  const fetchContent = async () => {
    try {
      setLoading(true);
      if (activeTab === 'news') {
        const response = await fetch(`${API_BASE_URL}/content/news?limit=50`);
        if (response.ok) {
          const data = await response.json();
          setNews(data);
        }
      } else if (activeTab === 'tutorials') {
        const response = await fetch(`${API_BASE_URL}/content/tutorials?limit=50`);
        if (response.ok) {
          const data = await response.json();
          setTutorials(data);
        }
      }
    } catch (error) {
      console.error('Erreur fetch content:', error);
      setError('Erreur de chargement du contenu');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteNews = async (newsId, title) => {
    const confirmDelete = window.confirm(
      `⚠️ ATTENTION ⚠️\n\nVoulez-vous vraiment supprimer cet article ?\n\n"${title}"\n\nCette action est IRRÉVERSIBLE.`
    );

    if (!confirmDelete) return;

    const confirmText = window.prompt(
      `Pour confirmer la suppression de l'article "${title}", tapez exactement : SUPPRIMER`
    );

    if (confirmText !== 'SUPPRIMER') {
      if (confirmText !== null) {
        alert('Confirmation incorrecte. Suppression annulée.');
      }
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/content/news/${newsId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess(data.message || 'Article supprimé avec succès');
        setError('');
        fetchContent(); // Refresh the list
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la suppression de l\'article');
      }
    } catch (error) {
      console.error('Erreur suppression news:', error);
      setError('Erreur de connexion lors de la suppression');
    }
  };

  const handleDeleteTutorial = async (tutorialId, title) => {
    const confirmDelete = window.confirm(
      `⚠️ ATTENTION ⚠️\n\nVoulez-vous vraiment supprimer ce tutoriel ?\n\n"${title}"\n\nCette action est IRRÉVERSIBLE.`
    );

    if (!confirmDelete) return;

    const confirmText = window.prompt(
      `Pour confirmer la suppression du tutoriel "${title}", tapez exactement : SUPPRIMER`
    );

    if (confirmText !== 'SUPPRIMER') {
      if (confirmText !== null) {
        alert('Confirmation incorrecte. Suppression annulée.');
      }
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/content/tutorials/${tutorialId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess(data.message || 'Tutoriel supprimé avec succès');
        setError('');
        fetchContent(); // Refresh the list
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la suppression du tutoriel');
      }
    } catch (error) {
      console.error('Erreur suppression tutorial:', error);
      setError('Erreur de connexion lors de la suppression');
    }
  };

  const fetchContentStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/content/stats/content`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setContentStats(data);
      }
    } catch (error) {
      console.error('Erreur fetch stats:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const endpoint = activeTab === 'news' ? '/content/news' : '/content/tutorials';
      const payload = activeTab === 'news' 
        ? {
            title: formData.title,
            content: formData.content,
            summary: formData.summary,
            tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag),
            is_pinned: formData.is_pinned
          }
        : {
            title: formData.title,
            description: formData.summary,
            game: formData.game,
            level: formData.level,
            content: formData.content,
            video_url: formData.video_url,
            tags: formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
          };

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        setSuccess(`${activeTab === 'news' ? 'Article' : 'Tutoriel'} créé avec succès !`);
        setShowCreateForm(false);
        setFormData({
          title: '',
          content: '',
          summary: '',
          tags: '',
          is_pinned: false,
          game: 'cs2',
          level: 'beginner',
          video_url: ''
        });
        fetchContent();
        fetchContentStats();
        setTimeout(() => setSuccess(''), 3000);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la création');
      }
    } catch (error) {
      setError('Erreur de connexion au serveur');
    }
  };

  const broadcastAnnouncement = async () => {
    const title = prompt('Titre de l\'annonce :');
    const message = prompt('Message de l\'annonce :');
    
    if (title && message) {
      try {
        const response = await fetch(`${API_BASE_URL}/admin/announcements/broadcast?title=${encodeURIComponent(title)}&message=${encodeURIComponent(message)}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          setSuccess('Annonce diffusée avec succès !');
          fetchContent();
          setTimeout(() => setSuccess(''), 3000);
        } else {
          setError('Erreur lors de la diffusion');
        }
      } catch (error) {
        setError('Erreur de connexion au serveur');
      }
    }
  };

  if (user?.role !== 'admin') {
    return (
      <div className="admin-container">
        <div className="access-denied">
          <h1>⛔ Accès refusé</h1>
          <p>Seuls les administrateurs peuvent gérer le contenu.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>📝 Gestion du Contenu</h1>
        <p>Gérez les articles, tutoriels et annonces</p>
      </div>

      {/* Statistiques rapides */}
      {contentStats && (
        <div className="admin-section">
          <h2>📊 Statistiques du contenu</h2>
          <div className="content-stats">
            <div className="stat-card">
              <div className="stat-icon">📰</div>
              <div className="stat-content">
                <h3>{contentStats.news.total}</h3>
                <p>Articles</p>
                <span>{contentStats.news.pinned} épinglés</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">📚</div>
              <div className="stat-content">
                <h3>{contentStats.tutorials.total}</h3>
                <p>Tutoriels</p>
                <span>{contentStats.tutorials.recent} récents</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">👀</div>
              <div className="stat-content">
                <h3>{contentStats.tutorials.top_viewed[0]?.views || 0}</h3>
                <p>Vues max</p>
                <span>Tutoriel populaire</span>
              </div>
            </div>
            <div className="stat-card growth">
              <div className="stat-icon">📈</div>
              <div className="stat-content">
                <h3>{contentStats.community_engagement.content_per_month}</h3>
                <p>Ce mois</p>
                <span>Nouvelles publications</span>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="admin-section">
        <div className="section-header">
          <div className="tab-buttons">
            <button 
              className={`tab-btn ${activeTab === 'news' ? 'active' : ''}`}
              onClick={() => setActiveTab('news')}
            >
              📰 Articles & News
            </button>
            <button 
              className={`tab-btn ${activeTab === 'tutorials' ? 'active' : ''}`}
              onClick={() => setActiveTab('tutorials')}
            >
              📚 Tutoriels
            </button>
          </div>

          <div className="action-buttons">
            <button 
              className="btn-broadcast"
              onClick={broadcastAnnouncement}
            >
              📢 Annonce importante
            </button>
            <button 
              className="btn-primary"
              onClick={() => setShowCreateForm(!showCreateForm)}
            >
              {showCreateForm ? '❌ Annuler' : `➕ Nouveau ${activeTab === 'news' ? 'article' : 'tutoriel'}`}
            </button>
          </div>
        </div>

        {/* Messages */}
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {/* Formulaire de création */}
        {showCreateForm && (
          <form onSubmit={handleSubmit} className="content-form">
            <div className="form-grid">
              <div className="form-group full-width">
                <label htmlFor="title">Titre</label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  required
                  placeholder={`Titre du ${activeTab === 'news' ? 'article' : 'tutoriel'}`}
                />
              </div>

              {activeTab === 'tutorials' && (
                <>
                  <div className="form-group">
                    <label htmlFor="game">Jeu</label>
                    <select
                      id="game"
                      name="game"
                      value={formData.game}
                      onChange={handleChange}
                      required
                    >
                      {games.map(game => (
                        <option key={game.id} value={game.id}>
                          {game.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="level">Niveau</label>
                    <select
                      id="level"
                      name="level"
                      value={formData.level}
                      onChange={handleChange}
                      required
                    >
                      {levels.map(level => (
                        <option key={level.id} value={level.id}>
                          {level.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="video_url">URL Vidéo (optionnel)</label>
                    <input
                      type="url"
                      id="video_url"
                      name="video_url"
                      value={formData.video_url}
                      onChange={handleChange}
                      placeholder="https://youtube.com/watch?v=..."
                    />
                  </div>
                </>
              )}

              <div className="form-group">
                <label htmlFor="summary">{activeTab === 'news' ? 'Résumé' : 'Description'}</label>
                <textarea
                  id="summary"
                  name="summary"
                  value={formData.summary}
                  onChange={handleChange}
                  required
                  placeholder={activeTab === 'news' ? 'Résumé de l\'article...' : 'Description du tutoriel...'}
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label htmlFor="tags">Tags (séparés par des virgules)</label>
                <input
                  type="text"
                  id="tags"
                  name="tags"
                  value={formData.tags}
                  onChange={handleChange}
                  placeholder="gaming, cs2, guide"
                />
              </div>

              {activeTab === 'news' && (
                <div className="form-group checkbox-group">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      name="is_pinned"
                      checked={formData.is_pinned}
                      onChange={handleChange}
                    />
                    📌 Épingler cet article
                  </label>
                </div>
              )}
            </div>

            <div className="form-group full-width">
              <label htmlFor="content">Contenu</label>
              <textarea
                id="content"
                name="content"
                value={formData.content}
                onChange={handleChange}
                required
                placeholder={activeTab === 'news' ? 'Contenu de l\'article...' : 'Contenu du tutoriel...'}
                rows="10"
              />
            </div>

            <button type="submit" className="btn-create">
              {activeTab === 'news' ? '📰 Publier l\'article' : '📚 Créer le tutoriel'}
            </button>
          </form>
        )}

        {/* Liste du contenu */}
        <div className="content-list">
          {loading ? (
            <div className="loading">Chargement du contenu...</div>
          ) : (
            <div className="content-items">
              {activeTab === 'news' ? (
                news.length === 0 ? (
                  <div className="empty-state">
                    <p>Aucun article publié pour le moment.</p>
                  </div>
                ) : (
                  news.map(article => (
                    <div key={article.id} className="content-card">
                      <div className="content-header">
                        <h3>{article.title}</h3>
                        <div className="content-meta">
                          {article.is_pinned && <span className="pinned-badge">📌 Épinglé</span>}
                          <span className="views">{article.views} vues</span>
                        </div>
                      </div>
                      <p className="content-summary">{article.summary}</p>
                      <div className="content-footer">
                        <div className="content-tags">
                          {article.tags.map((tag, index) => (
                            <span key={index} className="tag">#{tag}</span>
                          ))}
                        </div>
                        <div className="content-actions">
                          <div className="content-date">
                            {new Date(article.created_at).toLocaleDateString('fr-FR')}
                          </div>
                          <button
                            className="btn-delete-content"
                            onClick={() => handleDeleteNews(article.id, article.title)}
                            title="Supprimer cet article"
                          >
                            🗑️ Supprimer
                          </button>
                        </div>
                      </div>
                    </div>
                  ))
                )
              ) : (
                tutorials.length === 0 ? (
                  <div className="empty-state">
                    <p>Aucun tutoriel publié pour le moment.</p>
                  </div>
                ) : (
                  tutorials.map(tutorial => (
                    <div key={tutorial.id} className="content-card">
                      <div className="content-header">
                        <h3>{tutorial.title}</h3>
                        <div className="content-meta">
                          <span className="game-badge">{games.find(g => g.id === tutorial.game)?.name}</span>
                          <span className="level-badge">{levels.find(l => l.id === tutorial.level)?.name}</span>
                          <span className="views">{tutorial.views} vues • {tutorial.likes} ❤️</span>
                        </div>
                      </div>
                      <p className="content-summary">{tutorial.description}</p>
                      <div className="content-footer">
                        <div className="content-tags">
                          {tutorial.tags.map((tag, index) => (
                            <span key={index} className="tag">#{tag}</span>
                          ))}
                        </div>
                        <div className="content-actions">
                          <div className="content-date">
                            {new Date(tutorial.created_at).toLocaleDateString('fr-FR')}
                          </div>
                          <button
                            className="btn-delete-content"
                            onClick={() => handleDeleteTutorial(tutorial.id, tutorial.title)}
                            title="Supprimer ce tutoriel"
                          >
                            🗑️ Supprimer
                          </button>
                        </div>
                      </div>
                    </div>
                  ))
                )
              )}
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .admin-container {
          max-width: 1200px;
          margin: 40px auto;
          padding: 0 20px;
        }

        .admin-header {
          text-align: center;
          margin-bottom: 40px;
          padding: 30px;
          background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
          border-radius: 15px;
          color: white;
        }

        .admin-header h1 {
          margin: 0 0 10px 0;
          font-size: 32px;
          font-weight: 700;
        }

        .admin-section {
          background: white;
          border-radius: 15px;
          padding: 30px;
          margin-bottom: 30px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .content-stats {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 20px;
        }

        .stat-card {
          background: white;
          border-radius: 15px;
          padding: 20px;
          display: flex;
          align-items: center;
          gap: 15px;
          border: 2px solid #e5e7eb;
          transition: transform 0.3s;
        }

        .stat-card:hover {
          transform: translateY(-3px);
        }

        .stat-card.growth {
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          color: white;
          border-color: #059669;
        }

        .stat-icon {
          font-size: 32px;
          width: 50px;
          height: 50px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(59, 130, 246, 0.1);
          border-radius: 50%;
        }

        .growth .stat-icon {
          background: rgba(255, 255, 255, 0.2);
        }

        .stat-content h3 {
          margin: 0 0 5px 0;
          font-size: 24px;
          font-weight: 700;
          color: #1e3a8a;
        }

        .growth .stat-content h3 {
          color: white;
        }

        .stat-content p {
          margin: 0 0 3px 0;
          font-weight: 600;
          color: #1a1a1a;
        }

        .growth .stat-content p {
          color: rgba(255, 255, 255, 0.9);
        }

        .stat-content span {
          font-size: 12px;
          color: #333333;
        }

        .growth .stat-content span {
          color: rgba(255, 255, 255, 0.8);
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 25px;
          flex-wrap: wrap;
          gap: 15px;
        }

        .tab-buttons {
          display: flex;
          gap: 10px;
        }

        .tab-btn {
          background: #f1f5f9;
          color: #1a1a1a;
          border: 2px solid #e2e8f0;
          padding: 10px 20px;
          border-radius: 10px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .tab-btn.active {
          background: #3b82f6;
          color: white;
          border-color: #3b82f6;
        }

        .tab-btn:hover:not(.active) {
          background: #e2e8f0;
        }

        .action-buttons {
          display: flex;
          gap: 10px;
        }

        .btn-primary {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
          border: none;
          padding: 12px 20px;
          border-radius: 10px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-primary:hover {
          background: linear-gradient(45deg, #2563eb, #1e40af);
          transform: translateY(-2px);
        }

        .btn-broadcast {
          background: linear-gradient(45deg, #f59e0b, #d97706);
          color: white;
          border: none;
          padding: 12px 20px;
          border-radius: 10px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-broadcast:hover {
          background: linear-gradient(45deg, #d97706, #b45309);
          transform: translateY(-2px);
        }

        .content-form {
          background: #f8fafc;
          padding: 25px;
          border-radius: 12px;
          border: 2px solid #e2e8f0;
          margin-bottom: 30px;
        }

        .form-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 20px;
          margin-bottom: 20px;
        }

        .form-group {
          display: flex;
          flex-direction: column;
        }

        .form-group.full-width {
          grid-column: 1 / -1;
        }

        .form-group label {
          margin-bottom: 8px;
          font-weight: 600;
          color: #1a1a1a;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
          padding: 12px;
          border: 2px solid #e5e7eb;
          border-radius: 8px;
          font-size: 14px;
          transition: border-color 0.3s;
          color: #1a1a1a;
        }

        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
          outline: none;
          border-color: #3b82f6;
        }

        .checkbox-group {
          align-items: center;
          flex-direction: row;
        }

        .checkbox-label {
          display: flex;
          align-items: center;
          gap: 8px;
          cursor: pointer;
          font-weight: 600;
          color: #1a1a1a;
        }

        .btn-create {
          width: 100%;
          background: linear-gradient(45deg, #10b981, #059669);
          color: white;
          border: none;
          padding: 15px;
          border-radius: 10px;
          font-size: 16px;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-create:hover {
          background: linear-gradient(45deg, #059669, #047857);
          transform: translateY(-2px);
        }

        .content-items {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .content-card {
          background: #f8fafc;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          padding: 20px;
          transition: all 0.3s;
        }

        .content-card:hover {
          border-color: #3b82f6;
          transform: translateY(-2px);
        }

        .content-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 10px;
          gap: 15px;
        }

        .content-header h3 {
          margin: 0;
          color: #1e3a8a;
          font-size: 18px;
          font-weight: 600;
          flex: 1;
        }

        .content-meta {
          display: flex;
          gap: 10px;
          align-items: center;
          flex-wrap: wrap;
        }

        .pinned-badge {
          background: #fef3c7;
          color: #92400e;
          padding: 4px 8px;
          border-radius: 6px;
          font-size: 12px;
          font-weight: 600;
        }

        .game-badge {
          background: #3b82f6;
          color: white;
          padding: 4px 8px;
          border-radius: 6px;
          font-size: 12px;
          font-weight: 600;
        }

        .level-badge {
          background: #10b981;
          color: white;
          padding: 4px 8px;
          border-radius: 6px;
          font-size: 12px;
          font-weight: 600;
        }

        .views {
          color: #333333;
          font-size: 12px;
          font-weight: 600;
        }

        .content-summary {
          color: #1a1a1a;
          margin: 10px 0;
          line-height: 1.5;
        }

        .content-footer {
          display: flex;
          justify-content: space-between;
          align-items: flex-end;
          margin-top: 15px;
          flex-wrap: wrap;
          gap: 10px;
        }

        .content-actions {
          display: flex;
          align-items: center;
          gap: 15px;
        }

        .content-tags {
          display: flex;
          gap: 5px;
          flex-wrap: wrap;
        }

        .tag {
          background: #e2e8f0;
          color: #1a1a1a;
          padding: 2px 6px;
          border-radius: 4px;
          font-size: 11px;
          font-weight: 600;
        }

        .content-date {
          color: #6b7280;
          font-size: 14px;
        }

        .btn-delete-content {
          background: #ef4444;
          color: white;
          border: none;
          padding: 6px 12px;
          border-radius: 6px;
          font-size: 13px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.3s;
          display: flex;
          align-items: center;
          gap: 5px;
        }

        .btn-delete-content:hover {
          background: #dc2626;
          transform: translateY(-1px);
          box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
        }

        .error-message {
          background: #fee2e2;
          color: #dc2626;
          padding: 12px;
          border-radius: 8px;
          margin-bottom: 20px;
          border: 1px solid #fecaca;
        }

        .success-message {
          background: #dcfce7;
          color: #166534;
          padding: 12px;
          border-radius: 8px;
          margin-bottom: 20px;
          border: 1px solid #bbf7d0;
        }

        .loading, .empty-state {
          text-align: center;
          padding: 40px;
          color: #333333;
        }

        .access-denied {
          text-align: center;
          padding: 60px 20px;
          background: white;
          border-radius: 15px;
          margin: 40px 0;
        }

        .access-denied h1 {
          color: #dc2626;
          margin-bottom: 15px;
        }

        @media (max-width: 768px) {
          .admin-container {
            margin: 20px auto;
            padding: 0 15px;
          }

          .admin-section {
            padding: 20px;
          }

          .section-header {
            flex-direction: column;
            align-items: stretch;
          }

          .tab-buttons {
            justify-content: center;
          }

          .action-buttons {
            justify-content: center;
          }

          .form-grid {
            grid-template-columns: 1fr;
          }

          .content-header {
            flex-direction: column;
            align-items: stretch;
          }

          .content-footer {
            flex-direction: column;
            align-items: stretch;
          }

          .content-stats {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default AdminContent;