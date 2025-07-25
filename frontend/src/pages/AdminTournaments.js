import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const AdminTournaments = () => {
  const { user, token, API_BASE_URL } = useAuth();
  const [tournaments, setTournaments] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    game: 'cs2',
    tournament_type: 'elimination',
    max_participants: 16,
    entry_fee: 0,
    prize_pool: 0,
    registration_start: '',
    registration_end: '',
    tournament_start: '',
    rules: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const games = [
    { id: 'cs2', name: 'Counter-Strike 2' }
  ];

  const tournamentTypes = [
    { id: 'elimination', name: 'Élimination directe' },
    { id: 'bracket', name: 'Bracket' },
    { id: 'round_robin', name: 'Round Robin' }
  ];

  useEffect(() => {
    if (user?.role === 'admin') {
      fetchTournaments();
      fetchTemplates();
    }
  }, [user]);

  const fetchTournaments = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tournaments/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setTournaments(data);
      }
    } catch (error) {
      console.error('Erreur chargement tournois:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTemplates = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tournaments/templates/popular`);
      if (response.ok) {
        const data = await response.json();
        setTemplates(data.templates);
      }
    } catch (error) {
      console.error('Erreur chargement templates:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`${API_BASE_URL}/tournaments/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...formData,
          registration_start: new Date(formData.registration_start).toISOString(),
          registration_end: new Date(formData.registration_end).toISOString(),
          tournament_start: new Date(formData.tournament_start).toISOString()
        })
      });

      if (response.ok) {
        setSuccess('Tournoi créé avec succès !');
        setShowCreateForm(false);
        setFormData({
          title: '',
          description: '',
          game: 'cs2',
          tournament_type: 'elimination',
          max_participants: 16,
          entry_fee: 0,
          prize_pool: 0,
          registration_start: '',
          registration_end: '',
          tournament_start: '',
          rules: ''
        });
        fetchTournaments();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la création');
      }
    } catch (error) {
      setError('Erreur de connexion au serveur');
    }
  };

  const updateTournamentStatus = async (tournamentId, newStatus) => {
    try {
      const response = await fetch(`${API_BASE_URL}/tournaments/${tournamentId}/status?new_status=${newStatus}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        setSuccess(`Statut du tournoi mis à jour : ${newStatus}`);
        fetchTournaments();
      } else {
        setError('Erreur lors de la mise à jour du statut');
      }
    } catch (error) {
      setError('Erreur de connexion au serveur');
    }
  };

  const deleteTournament = async (tournamentId, tournamentTitle) => {
    // Confirmation avant suppression
    const confirmDelete = window.confirm(
      `⚠️ Êtes-vous sûr de vouloir supprimer le tournoi "${tournamentTitle}" ?\n\n` +
      `Cette action est irréversible et supprimera :\n` +
      `• Le tournoi et toutes ses données\n` +
      `• Les inscriptions des participants\n` +
      `• L'historique associé\n\n` +
      `Tapez "SUPPRIMER" pour confirmer :`
    );

    if (!confirmDelete) return;

    // Double confirmation avec saisie
    const confirmText = window.prompt(
      `Pour confirmer la suppression du tournoi "${tournamentTitle}", tapez exactement : SUPPRIMER`
    );

    if (confirmText !== 'SUPPRIMER') {
      if (confirmText !== null) { // User didn't cancel
        setError('Confirmation incorrecte. Suppression annulée.');
      }
      return;
    }

    try {
      setError('');
      setSuccess('');

      const response = await fetch(`${API_BASE_URL}/tournaments/${tournamentId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess(`✅ ${data.message}`);
        fetchTournaments(); // Actualiser la liste
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la suppression');
      }
    } catch (error) {
      setError('Erreur de connexion au serveur');
    }
  };

  const useTemplate = (template) => {
    const now = new Date();
    const registrationStart = new Date(now.getTime() + 24 * 60 * 60 * 1000); // +1 jour
    const registrationEnd = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000); // +7 jours  
    const tournamentStart = new Date(now.getTime() + 8 * 24 * 60 * 60 * 1000); // +8 jours

    setFormData({
      title: template.name,
      description: template.description,
      game: template.game,
      tournament_type: template.tournament_type,
      max_participants: template.max_participants,
      entry_fee: 0,
      prize_pool: 0,
      registration_start: registrationStart.toISOString().slice(0, 16),
      registration_end: registrationEnd.toISOString().slice(0, 16),
      tournament_start: tournamentStart.toISOString().slice(0, 16),
      rules: template.rules
    });
    setShowCreateForm(true);
  };

  if (user?.role !== 'admin') {
    return (
      <div className="admin-container">
        <div className="access-denied">
          <h1>⛔ Accès refusé</h1>
          <p>Seuls les administrateurs peuvent gérer les tournois.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>🏆 Gestion des Tournois</h1>
        <p>Créez et gérez les tournois de la communauté</p>
      </div>

      <div className="admin-section">
        <div className="section-header">
          <h2>⚡ Actions rapides</h2>
          <button 
            className="btn-primary"
            onClick={() => setShowCreateForm(!showCreateForm)}
          >
            {showCreateForm ? '❌ Annuler' : '➕ Nouveau tournoi'}
          </button>
        </div>

        {/* Messages */}
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {/* Templates CS2 populaires */}
        {!showCreateForm && (
          <div className="templates-section">
            <h3>🎯 Templates CS2 Spécialisés</h3>
            <p style={{color: '#64748b', marginBottom: '20px'}}>
              Choisissez parmi nos formats de tournois CS2 optimisés pour Oupafamilly
            </p>
            <div className="templates-grid">
              {templates.map((template, index) => (
                <div key={index} className="template-card">
                  <div className="template-header">
                    <h4>{template.name}</h4>
                    <span className="game-badge">{games.find(g => g.id === template.game)?.name}</span>
                  </div>
                  <p>{template.description}</p>
                  <div className="template-details">
                    <span>👥 {template.max_participants} participants</span>
                    <span>⏱️ {template.suggested_duration_hours}h</span>
                  </div>
                  <div className="template-rules">
                    <details>
                      <summary>📋 Voir les règles détaillées</summary>
                      <div className="rules-content">
                        {template.rules.split('\n').map((line, idx) => 
                          line.trim() && (
                            <div key={idx} className="rule-line">
                              {line}
                            </div>
                          )
                        )}
                      </div>
                    </details>
                  </div>
                  <button 
                    className="btn-template"
                    onClick={() => useTemplate(template)}
                  >
                    Utiliser ce template
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Formulaire de création */}
        {showCreateForm && (
          <form onSubmit={handleSubmit} className="tournament-form">
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="title">Titre du tournoi</label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  required
                  placeholder="Nom du tournoi"
                />
              </div>

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
                <label htmlFor="tournament_type">Type de tournoi</label>
                <select
                  id="tournament_type"
                  name="tournament_type"
                  value={formData.tournament_type}
                  onChange={handleChange}
                  required
                >
                  {tournamentTypes.map(type => (
                    <option key={type.id} value={type.id}>
                      {type.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="max_participants">Participants max</label>
                <input
                  type="number"
                  id="max_participants"
                  name="max_participants"
                  value={formData.max_participants}
                  onChange={handleChange}
                  required
                  min="2"
                  max="64"
                />
              </div>

              <div className="form-group">
                <label htmlFor="entry_fee">Frais d'inscription (€)</label>
                <input
                  type="number"
                  id="entry_fee"
                  name="entry_fee"
                  value={formData.entry_fee}
                  onChange={handleChange}
                  min="0"
                  step="0.01"
                />
              </div>

              <div className="form-group">
                <label htmlFor="prize_pool">Dotation (€)</label>
                <input
                  type="number"
                  id="prize_pool"
                  name="prize_pool"
                  value={formData.prize_pool}
                  onChange={handleChange}
                  min="0"
                  step="0.01"
                />
              </div>

              <div className="form-group">
                <label htmlFor="registration_start">Début des inscriptions</label>
                <input
                  type="datetime-local"
                  id="registration_start"
                  name="registration_start"
                  value={formData.registration_start}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="registration_end">Fin des inscriptions</label>
                <input
                  type="datetime-local"
                  id="registration_end"
                  name="registration_end"
                  value={formData.registration_end}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="tournament_start">Début du tournoi</label>
                <input
                  type="datetime-local"
                  id="tournament_start"
                  name="tournament_start"
                  value={formData.tournament_start}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="form-group full-width">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                required
                placeholder="Description du tournoi..."
                rows="3"
              />
            </div>

            <div className="form-group full-width">
              <label htmlFor="rules">Règlement</label>
              <textarea
                id="rules"
                name="rules"
                value={formData.rules}
                onChange={handleChange}
                required
                placeholder="Règles du tournoi..."
                rows="5"
              />
            </div>

            <button type="submit" className="btn-create">
              🏆 Créer le tournoi
            </button>
          </form>
        )}
      </div>

      {/* Liste des tournois existants */}
      <div className="admin-section">
        <h2>📋 Tournois existants</h2>
        
        {loading ? (
          <div className="loading">Chargement des tournois...</div>
        ) : tournaments.length === 0 ? (
          <div className="empty-state">
            <p>Aucun tournoi créé pour le moment.</p>
            <button 
              className="btn-primary"
              onClick={() => setShowCreateForm(true)}
            >
              Créer le premier tournoi
            </button>
          </div>
        ) : (
          <div className="tournaments-list">
            {tournaments.map(tournament => (
              <div key={tournament.id} className="tournament-card">
                <div className="tournament-header">
                  <h3>{tournament.title}</h3>
                  <span className={`status-badge ${tournament.status}`}>
                    {tournament.status === 'draft' && '📝 Brouillon'}
                    {tournament.status === 'open' && '🟢 Ouvert'}
                    {tournament.status === 'in_progress' && '⏳ En cours'}
                    {tournament.status === 'completed' && '✅ Terminé'}
                    {tournament.status === 'cancelled' && '❌ Annulé'}
                  </span>
                </div>
                
                <div className="tournament-info">
                  <div className="info-row">
                    <span>🎮 {games.find(g => g.id === tournament.game)?.name}</span>
                    <span>👥 {tournament.participants.length}/{tournament.max_participants}</span>
                    <span>💰 {tournament.prize_pool}€</span>
                  </div>
                  <div className="info-row">
                    <span>📅 {new Date(tournament.tournament_start).toLocaleDateString('fr-FR')}</span>
                    <span>⏰ {new Date(tournament.tournament_start).toLocaleTimeString('fr-FR', {hour: '2-digit', minute: '2-digit'})}</span>
                  </div>
                </div>

                <div className="tournament-actions">
                  {tournament.status === 'draft' && (
                    <button 
                      className="btn-action open"
                      onClick={() => updateTournamentStatus(tournament.id, 'open')}
                    >
                      🟢 Ouvrir les inscriptions
                    </button>
                  )}
                  {tournament.status === 'open' && (
                    <button 
                      className="btn-action start"
                      onClick={() => updateTournamentStatus(tournament.id, 'in_progress')}
                    >
                      ▶️ Commencer le tournoi
                    </button>
                  )}
                  {tournament.status === 'in_progress' && (
                    <button 
                      className="btn-action complete"
                      onClick={() => updateTournamentStatus(tournament.id, 'completed')}
                    >
                      ✅ Terminer le tournoi
                    </button>
                  )}
                  <button 
                    className="btn-action cancel"
                    onClick={() => updateTournamentStatus(tournament.id, 'cancelled')}
                  >
                    ❌ Annuler
                  </button>
                  <button 
                    className="btn-action delete"
                    onClick={() => deleteTournament(tournament.id, tournament.title)}
                    disabled={tournament.status === 'in_progress'}
                    title={tournament.status === 'in_progress' ? 'Impossible de supprimer un tournoi en cours' : 'Supprimer définitivement ce tournoi'}
                  >
                    🗑️ Supprimer
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
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

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 25px;
        }

        .section-header h2 {
          margin: 0;
          color: #1e3a8a;
          font-size: 24px;
          font-weight: 600;
        }

        .btn-primary {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 10px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-primary:hover {
          background: linear-gradient(45deg, #2563eb, #1e40af);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
        }

        .templates-section {
          margin-bottom: 30px;
        }

        .templates-section h3 {
          color: #1e3a8a;
          margin-bottom: 20px;
        }

        .templates-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 20px;
        }

        .template-card {
          background: #f8fafc;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          padding: 20px;
          transition: all 0.3s;
        }

        .template-card:hover {
          border-color: #3b82f6;
          transform: translateY(-2px);
        }

        .template-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 10px;
        }

        .template-header h4 {
          margin: 0;
          color: #1e3a8a;
          font-size: 18px;
        }

        .game-badge {
          background: #3b82f6;
          color: white;
          padding: 4px 8px;
          border-radius: 6px;
          font-size: 12px;
          font-weight: 600;
        }

        .template-details {
          display: flex;
          gap: 15px;
          margin: 15px 0;
          font-size: 14px;
          color: #333333;
        }

        .template-rules {
          margin: 15px 0;
        }

        .template-rules details {
          cursor: pointer;
        }

        .template-rules summary {
          font-weight: 600;
          color: #1e3a8a;
          padding: 8px 12px;
          background: #f1f5f9;
          border-radius: 6px;
          border: 1px solid #e2e8f0;
          outline: none;
          user-select: none;
        }

        .template-rules summary:hover {
          background: #e2e8f0;
        }

        .rules-content {
          margin-top: 10px;
          padding: 15px;
          background: #fafbfc;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          max-height: 200px;
          overflow-y: auto;
        }

        .rule-line {
          font-size: 13px;
          line-height: 1.4;
          color: #1a1a1a;
          margin-bottom: 4px;
        }

        .btn-template {
          width: 100%;
          background: #1e3a8a;
          color: white;
          border: none;
          padding: 10px;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
          transition: background 0.3s;
        }

        .btn-template:hover {
          background: #1e40af;
        }

        .tournament-form {
          background: #f8fafc;
          padding: 25px;
          border-radius: 12px;
          border: 2px solid #e2e8f0;
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

        .btn-create {
          width: 100%;
          background: linear-gradient(45deg, #10b981, #059669);
          color: white;
          border: none;
          padding: 15px;
          border-radius: 10px;
          font-size: 18px;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-create:hover {
          background: linear-gradient(45deg, #059669, #047857);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
        }

        .tournaments-list {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .tournament-card {
          background: #f8fafc;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          padding: 25px;
        }

        .tournament-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 15px;
        }

        .tournament-header h3 {
          margin: 0;
          color: #1e3a8a;
          font-size: 20px;
        }

        .status-badge {
          padding: 6px 12px;
          border-radius: 20px;
          font-size: 14px;
          font-weight: 600;
        }

        .status-badge.draft {
          background: #fef3c7;
          color: #92400e;
        }

        .status-badge.open {
          background: #dcfce7;
          color: #166534;
        }

        .status-badge.in_progress {
          background: #dbeafe;
          color: #1e40af;
        }

        .status-badge.completed {
          background: #f3e8ff;
          color: #7c3aed;
        }

        .status-badge.cancelled {
          background: #fee2e2;
          color: #dc2626;
        }

        .tournament-info {
          margin-bottom: 20px;
        }

        .info-row {
          display: flex;
          gap: 20px;
          margin-bottom: 8px;
          font-size: 14px;
          color: #333333;
        }

        .tournament-actions {
          display: flex;
          gap: 10px;
          flex-wrap: wrap;
        }

        .btn-action {
          padding: 8px 16px;
          border: none;
          border-radius: 6px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-action.open {
          background: #dcfce7;
          color: #166534;
        }

        .btn-action.start {
          background: #dbeafe;
          color: #1e40af;
        }

        .btn-action.complete {
          background: #f3e8ff;
          color: #7c3aed;
        }

        .btn-action.cancel {
          background: #fee2e2;
          color: #dc2626;
        }

        .btn-action.delete {
          background: #7f1d1d;
          color: #fecaca;
          border: 1px solid #dc2626;
        }

        .btn-action.delete:hover:not(:disabled) {
          background: #991b1b;
          color: white;
        }

        .btn-action.delete:disabled {
          opacity: 0.5;
          cursor: not-allowed;
          background: #f3f4f6;
          color: #9ca3af;
        }

        .btn-action:hover {
          transform: translateY(-1px);
          opacity: 0.9;
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
            gap: 15px;
            align-items: stretch;
          }

          .form-grid {
            grid-template-columns: 1fr;
          }

          .tournament-header {
            flex-direction: column;
            gap: 10px;
            align-items: stretch;
          }

          .tournament-actions {
            justify-content: center;
          }

          .templates-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default AdminTournaments;