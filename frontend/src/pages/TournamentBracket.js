import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const TournamentBracket = () => {
  const { id } = useParams();
  const [tournament, setTournament] = useState(null);
  const [bracket, setBracket] = useState({ rounds: [], tournament_status: 'loading' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [matchResult, setMatchResult] = useState({
    winner_id: '',
    player1_score: 0,
    player2_score: 0,
    notes: ''
  });
  const { API_BASE_URL, user, token } = useAuth();

  useEffect(() => {
    fetchTournamentInfo();
    fetchBracket();
  }, [id]);

  const fetchTournamentInfo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tournaments/${id}`);
      if (response.ok) {
        const data = await response.json();
        setTournament(data);
      }
    } catch (error) {
      console.error('Error fetching tournament info:', error);
    }
  };

  const fetchBracket = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/matches/tournament/${id}/bracket`);
      
      if (response.ok) {
        const data = await response.json();
        setBracket(data);
      } else {
        setError('Erreur lors du chargement du bracket');
      }
    } catch (error) {
      console.error('Error fetching bracket:', error);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const generateBracket = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/matches/tournament/${id}/generate-bracket`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.message);
        fetchBracket();
        fetchTournamentInfo();
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Erreur lors de la génération du bracket');
      }
    } catch (error) {
      console.error('Error generating bracket:', error);
      alert('Erreur de connexion au serveur');
    }
  };

  const updateMatchResult = async () => {
    if (!selectedMatch || !matchResult.winner_id) {
      alert('Veuillez sélectionner un gagnant');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/matches/${selectedMatch.id}/result`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          winner_id: matchResult.winner_id,
          player1_score: parseInt(matchResult.player1_score) || 0,
          player2_score: parseInt(matchResult.player2_score) || 0,
          notes: matchResult.notes
        })
      });

      if (response.ok) {
        alert('Résultat mis à jour avec succès !');
        setSelectedMatch(null);
        setMatchResult({ winner_id: '', player1_score: 0, player2_score: 0, notes: '' });
        fetchBracket();
        fetchTournamentInfo();
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Erreur lors de la mise à jour');
      }
    } catch (error) {
      console.error('Error updating match result:', error);
      alert('Erreur de connexion au serveur');
    }
  };

  const getPlayerName = (match, isPlayer1 = true) => {
    const playerName = isPlayer1 ? match.player1_name : match.player2_name;
    const playerType = isPlayer1 ? match.player1_type : match.player2_type;
    
    if (!playerName || playerName === 'TBD') return 'TBD';
    if (playerName.includes('Winner of')) return playerName;
    if (playerName === 'BYE') return 'BYE';
    
    // Return the enriched name from backend
    return playerName;
  };

  const getPlayerTypeIcon = (match, isPlayer1 = true) => {
    const playerType = isPlayer1 ? match.player1_type : match.player2_type;
    
    switch(playerType) {
      case 'team':
        return '👥';
      case 'user':
        return '👤';
      case 'placeholder':
        return '🏆';
      default:
        return '❓';
    }
  };

  const getMatchStatusBadge = (match) => {
    switch (match.status) {
      case 'scheduled':
        return <span className="status-badge scheduled">📅 Programmé</span>;
      case 'in_progress':
        return <span className="status-badge in-progress">⏳ En cours</span>;
      case 'completed':
        return <span className="status-badge completed">✅ Terminé</span>;
      case 'cancelled':
        return <span className="status-badge cancelled">❌ Annulé</span>;
      default:
        return <span className="status-badge">❓ Inconnu</span>;
    }
  };

  const canManageMatch = () => {
    return user && (user.role === 'admin' || user.role === 'moderator');
  };

  if (loading) {
    return (
      <div className="bracket-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Chargement du bracket...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bracket-container">
      <div className="bracket-header">
        <div className="header-info">
          <Link to={`/tournois/${id}`} className="btn-back">
            ← Retour au tournoi
          </Link>
          <h1>🏆 Bracket - {tournament?.title}</h1>
          <div className="tournament-info">
            <span className="status-badge">Statut: {tournament?.status}</span>
            {tournament?.winner_id && bracket.participants_map ? (
              <span className="winner-badge">
                🏆 Vainqueur: {bracket.participants_map[tournament.winner_id]?.display_name || 
                              `Joueur ${tournament.winner_id.substring(0, 8)}`}
              </span>
            ) : tournament?.winner_id ? (
              <span className="winner-badge">
                🏆 Vainqueur: Joueur {tournament.winner_id.substring(0, 8)}
              </span>
            ) : null}
          </div>
        </div>
        
        {canManageMatch() && bracket.tournament_status !== 'completed' && (
          <div className="admin-actions">
            {bracket.rounds.length === 0 ? (
              <button className="btn-generate" onClick={generateBracket}>
                🎲 Générer le Bracket Aléatoire
              </button>
            ) : (
              <p className="bracket-info">Bracket généré avec {bracket.rounds.length} rounds</p>
            )}
          </div>
        )}
      </div>

      {error && (
        <div className="error-banner">
          ❌ {error}
          <button onClick={fetchBracket}>🔄 Réessayer</button>
        </div>
      )}

      {bracket.rounds.length === 0 ? (
        <div className="no-bracket">
          <div className="no-bracket-icon">🏆</div>
          <h3>Bracket non généré</h3>
          <p>Le bracket du tournoi n'a pas encore été généré.</p>
          {canManageMatch() ? (
            <button className="btn-generate-large" onClick={generateBracket}>
              🎲 Générer le Bracket Maintenant
            </button>
          ) : (
            <p>Attendez que l'organisateur génère le bracket.</p>
          )}
        </div>
      ) : (
        <div className="bracket-grid">
          {bracket.rounds.map((round, roundIndex) => (
            <div key={round.round_number} className="bracket-round">
              <div className="round-header">
                <h3>
                  {round.round_number === bracket.rounds.length ? '🏆 Finale' : 
                   round.round_number === bracket.rounds.length - 1 ? '🥈 Demi-finale' :
                   `Round ${round.round_number}`}
                </h3>
                <span className="matches-count">{round.matches.length} match(s)</span>
              </div>
              
              <div className="matches-list">
                {round.matches.map((match, matchIndex) => (
                  <div 
                    key={match.id} 
                    className={`match-card ${match.status} ${selectedMatch?.id === match.id ? 'selected' : ''}`}
                    onClick={() => canManageMatch() && match.status === 'scheduled' && setSelectedMatch(match)}
                  >
                    <div className="match-header">
                      <span className="match-number">Match #{match.match_number}</span>
                      {getMatchStatusBadge(match)}
                    </div>
                    
                    <div className="match-players">
                      <div className={`player ${match.winner_id === match.player1_id ? 'winner' : ''}`}>
                        <div className="player-info">
                          <span className="player-icon">{getPlayerTypeIcon(match, true)}</span>
                          <span className="player-name">{getPlayerName(match, true)}</span>
                        </div>
                        {match.status === 'completed' && (
                          <span className="player-score">{match.player1_score}</span>
                        )}
                      </div>
                      
                      <div className="vs-divider">VS</div>
                      
                      <div className={`player ${match.winner_id === match.player2_id ? 'winner' : ''}`}>
                        <div className="player-info">
                          <span className="player-icon">{getPlayerTypeIcon(match, false)}</span>
                          <span className="player-name">{getPlayerName(match, false)}</span>
                        </div>
                        {match.status === 'completed' && (
                          <span className="player-score">{match.player2_score}</span>
                        )}
                      </div>
                    </div>
                    
                    {match.status === 'completed' && match.notes && (
                      <div className="match-notes">
                        📝 {match.notes}
                      </div>
                    )}
                    
                    {canManageMatch() && match.status === 'scheduled' && (
                      <div className="match-action">
                        👆 Cliquer pour saisir le résultat
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Match Result Modal */}
      {selectedMatch && (
        <div className="modal-overlay" onClick={() => setSelectedMatch(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>🏆 Résultat du Match #{selectedMatch.match_number}</h2>
              <button 
                className="modal-close"
                onClick={() => setSelectedMatch(null)}
              >
                ×
              </button>
            </div>

            <div className="modal-body">
              <div className="match-participants">
                <h3>Participants</h3>
                <div className="participants-grid">
                  <div className="participant">
                    <div className="participant-header">
                      <span className="participant-icon">{getPlayerTypeIcon(selectedMatch, true)}</span>
                      <span className="participant-name">{getPlayerName(selectedMatch, true)}</span>
                    </div>
                    <input
                      type="number"
                      placeholder="Score"
                      value={matchResult.player1_score}
                      onChange={(e) => setMatchResult({...matchResult, player1_score: e.target.value})}
                      className="score-input"
                    />
                  </div>
                  <div className="vs-text">VS</div>
                  <div className="participant">
                    <div className="participant-header">
                      <span className="participant-icon">{getPlayerTypeIcon(selectedMatch, false)}</span>
                      <span className="participant-name">{getPlayerName(selectedMatch, false)}</span>
                    </div>
                    <input
                      type="number"
                      placeholder="Score"
                      value={matchResult.player2_score}
                      onChange={(e) => setMatchResult({...matchResult, player2_score: e.target.value})}
                      className="score-input"
                    />
                  </div>
                </div>
              </div>

              <div className="winner-selection">
                <h3>🏆 Gagnant</h3>
                <div className="winner-options">
                  <label className="winner-option">
                    <input
                      type="radio"
                      name="winner"
                      value={selectedMatch.player1_id}
                      checked={matchResult.winner_id === selectedMatch.player1_id}
                      onChange={(e) => setMatchResult({...matchResult, winner_id: e.target.value})}
                    />
                    <div className="winner-info">
                      <span className="winner-icon">{getPlayerTypeIcon(selectedMatch, true)}</span>
                      <span>{getPlayerName(selectedMatch, true)}</span>
                    </div>
                  </label>
                  <label className="winner-option">
                    <input
                      type="radio"
                      name="winner"
                      value={selectedMatch.player2_id}
                      checked={matchResult.winner_id === selectedMatch.player2_id}
                      onChange={(e) => setMatchResult({...matchResult, winner_id: e.target.value})}
                    />
                    <div className="winner-info">
                      <span className="winner-icon">{getPlayerTypeIcon(selectedMatch, false)}</span>
                      <span>{getPlayerName(selectedMatch, false)}</span>
                    </div>
                  </label>
                </div>
              </div>

              <div className="match-notes-section">
                <h3>📝 Notes (optionnel)</h3>
                <textarea
                  placeholder="Commentaires sur le match..."
                  value={matchResult.notes}
                  onChange={(e) => setMatchResult({...matchResult, notes: e.target.value})}
                  className="notes-textarea"
                  rows="3"
                />
              </div>
            </div>

            <div className="modal-footer">
              <button 
                className="btn-cancel"
                onClick={() => setSelectedMatch(null)}
              >
                Annuler
              </button>
              <button 
                className="btn-confirm"
                onClick={updateMatchResult}
                disabled={!matchResult.winner_id}
              >
                🏆 Confirmer le Résultat
              </button>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        .bracket-container {
          max-width: 1400px;
          margin: 40px auto;
          padding: 0 20px;
        }

        .bracket-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 30px;
          flex-wrap: wrap;
          gap: 20px;
        }

        .header-info h1 {
          color: #1e3a8a;
          font-size: 32px;
          font-weight: 800;
          margin: 10px 0;
        }

        .tournament-info {
          display: flex;
          gap: 15px;
          align-items: center;
          flex-wrap: wrap;
        }

        .btn-back {
          background: #f1f5f9;
          color: #1e3a8a;
          padding: 10px 20px;
          border-radius: 10px;
          text-decoration: none;
          font-weight: 600;
          transition: all 0.3s;
        }

        .btn-back:hover {
          background: #e2e8f0;
          transform: translateY(-1px);
        }

        .btn-generate, .btn-generate-large {
          background: linear-gradient(45deg, #10b981, #059669);
          color: white;
          border: none;
          padding: 15px 25px;
          border-radius: 12px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
          font-size: 16px;
        }

        .btn-generate-large {
          padding: 20px 40px;
          font-size: 18px;
        }

        .btn-generate:hover, .btn-generate-large:hover {
          background: linear-gradient(45deg, #059669, #047857);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
        }

        .status-badge {
          padding: 6px 12px;
          border-radius: 20px;
          font-size: 14px;
          font-weight: 600;
        }

        .status-badge.scheduled {
          background: #dbeafe;
          color: #1e40af;
        }

        .status-badge.in-progress {
          background: #fef3c7;
          color: #92400e;
        }

        .status-badge.completed {
          background: #dcfce7;
          color: #166534;
        }

        .status-badge.cancelled {
          background: #fee2e2;
          color: #dc2626;
        }

        .winner-badge {
          background: linear-gradient(45deg, #fbbf24, #f59e0b);
          color: white;
          padding: 8px 15px;
          border-radius: 15px;
          font-weight: 700;
          font-size: 14px;
        }

        .no-bracket {
          text-align: center;
          padding: 80px 20px;
          background: white;
          border-radius: 20px;
          margin: 40px 0;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .no-bracket-icon {
          font-size: 100px;
          margin-bottom: 20px;
        }

        .no-bracket h3 {
          color: #1e3a8a;
          font-size: 28px;
          margin-bottom: 15px;
        }

        .bracket-grid {
          display: flex;
          gap: 30px;
          overflow-x: auto;
          padding: 20px 0;
          min-height: 500px;
        }

        .bracket-round {
          min-width: 300px;
          background: white;
          border-radius: 15px;
          padding: 20px;
          box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
          border: 2px solid #e5e7eb;
        }

        .round-header {
          text-align: center;
          margin-bottom: 25px;
          padding-bottom: 15px;
          border-bottom: 2px solid #e5e7eb;
        }

        .round-header h3 {
          color: #1e3a8a;
          font-size: 20px;
          font-weight: 700;
          margin: 0 0 5px 0;
        }

        .matches-count {
          color: #64748b;
          font-size: 14px;
        }

        .matches-list {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }

        .match-card {
          background: #f8fafc;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          padding: 15px;
          transition: all 0.3s;
          cursor: pointer;
        }

        .match-card:hover {
          border-color: #3b82f6;
          transform: translateY(-2px);
        }

        .match-card.selected {
          border-color: #10b981;
          background: #ecfdf5;
        }

        .match-card.completed {
          border-color: #16a34a;
        }

        .match-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 15px;
        }

        .match-number {
          font-weight: 700;
          color: #1e3a8a;
          font-size: 14px;
        }

        .match-players {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .player {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 8px 12px;
          background: white;
          border-radius: 8px;
          border: 1px solid #e5e7eb;
          transition: all 0.3s;
        }

        .player.winner {
          background: linear-gradient(45deg, #dcfce7, #bbf7d0);
          border-color: #16a34a;
          font-weight: 700;
        }

        .player-info {
          display: flex;
          align-items: center;
          gap: 8px;
          flex: 1;
        }

        .player-icon {
          font-size: 14px;
          min-width: 16px;
        }

        .player-name {
          font-size: 14px;
          color: #1a1a1a;
          flex: 1;
        }

        .player-score {
          background: #1e3a8a;
          color: white;
          padding: 4px 8px;
          border-radius: 6px;
          font-weight: 700;
          font-size: 12px;
        }

        .vs-divider {
          text-align: center;
          font-weight: 700;
          color: #64748b;
          font-size: 12px;
          margin: 5px 0;
        }

        .match-notes {
          margin-top: 10px;
          padding: 8px 12px;
          background: #f1f5f9;
          border-radius: 8px;
          font-size: 12px;
          color: #475569;
          font-style: italic;
        }

        .match-action {
          margin-top: 10px;
          text-align: center;
          color: #10b981;
          font-size: 12px;
          font-weight: 600;
        }

        /* Modal Styles */
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.7);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }

        .modal-content {
          background: white;
          border-radius: 20px;
          width: 90%;
          max-width: 600px;
          max-height: 90vh;
          overflow-y: auto;
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }

        .modal-header {
          padding: 25px 25px 0;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 2px solid #f1f5f9;
          margin-bottom: 25px;
        }

        .modal-header h2 {
          color: #1e3a8a;
          font-size: 24px;
          font-weight: 700;
          margin: 0;
        }

        .modal-close {
          background: none;
          border: none;
          font-size: 30px;
          color: #64748b;
          cursor: pointer;
          padding: 0;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s;
        }

        .modal-close:hover {
          background: #f1f5f9;
          color: #1a1a1a;
        }

        .modal-body {
          padding: 0 25px;
        }

        .match-participants h3,
        .winner-selection h3,
        .match-notes-section h3 {
          color: #1e3a8a;
          font-size: 18px;
          font-weight: 700;
          margin-bottom: 15px;
        }

        .participants-grid {
          display: grid;
          grid-template-columns: 1fr auto 1fr;
          gap: 15px;
          align-items: center;
          margin-bottom: 25px;
        }

        .participant {
          display: flex;
          flex-direction: column;
          gap: 8px;
          align-items: center;
        }

        .participant-header {
          display: flex;
          align-items: center;
          gap: 8px;
          text-align: center;
        }

        .participant-icon {
          font-size: 16px;
        }

        .participant-name {
          font-weight: 700;
          color: #1a1a1a;
          text-align: center;
          font-size: 15px;
        }

        .score-input {
          width: 80px;
          padding: 8px 12px;
          border: 2px solid #e5e7eb;
          border-radius: 8px;
          text-align: center;
          font-weight: 700;
          font-size: 16px;
          background: white;
          color: #1a1a1a;
        }

        .score-input:focus {
          outline: none;
          border-color: #3b82f6;
        }

        .vs-text {
          font-weight: 700;
          color: #1a1a1a;
          text-align: center;
          font-size: 16px;
        }

        .winner-options {
          display: flex;
          flex-direction: column;
          gap: 10px;
          margin-bottom: 25px;
        }

        .winner-option {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 12px 15px;
          border: 2px solid #e5e7eb;
          border-radius: 10px;
          cursor: pointer;
          transition: all 0.3s;
          background: white;
        }

        .winner-option:hover {
          border-color: #3b82f6;
          background: #f8fafc;
        }

        .winner-option input {
          width: 18px;
          height: 18px;
        }

        .winner-info {
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 700;
          color: #1a1a1a;
          font-size: 15px;
        }

        .winner-icon {
          font-size: 16px;
        }

        .notes-textarea {
          width: 100%;
          padding: 12px 15px;
          border: 2px solid #e5e7eb;
          border-radius: 10px;
          font-family: inherit;
          resize: vertical;
          margin-bottom: 25px;
          background: white;
          color: #1a1a1a;
          font-weight: 500;
          font-size: 14px;
        }

        .notes-textarea:focus {
          outline: none;
          border-color: #3b82f6;
        }

        .notes-textarea::placeholder {
          color: #6b7280;
          font-weight: 400;
        }

        .modal-footer {
          padding: 25px;
          display: flex;
          gap: 15px;
          justify-content: flex-end;
          border-top: 2px solid #f1f5f9;
          margin-top: 25px;
        }

        .btn-cancel {
          background: #f1f5f9;
          color: #64748b;
          border: 2px solid #e5e7eb;
          padding: 12px 25px;
          border-radius: 10px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-cancel:hover {
          background: #e2e8f0;
          color: #1a1a1a;
        }

        .btn-confirm {
          background: linear-gradient(45deg, #10b981, #059669);
          color: white;
          border: none;
          padding: 12px 25px;
          border-radius: 10px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-confirm:hover:not(:disabled) {
          background: linear-gradient(45deg, #059669, #047857);
          transform: translateY(-1px);
          box-shadow: 0 3px 10px rgba(16, 185, 129, 0.3);
        }

        .btn-confirm:disabled {
          opacity: 0.5;
          cursor: not-allowed;
          transform: none;
        }

        .loading-state, .error-banner {
          text-align: center;
          padding: 40px 20px;
          margin: 20px 0;
          border-radius: 15px;
        }

        .loading-state {
          background: white;
        }

        .error-banner {
          background: #fee2e2;
          color: #dc2626;
          border: 1px solid #fecaca;
        }

        .spinner {
          width: 50px;
          height: 50px;
          border: 4px solid #e5e7eb;
          border-top: 4px solid #3b82f6;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin: 0 auto 20px;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
          .bracket-container {
            margin: 20px auto;
            padding: 0 15px;
          }

          .bracket-header {
            flex-direction: column;
            align-items: stretch;
          }

          .bracket-grid {
            flex-direction: column;
            gap: 20px;
          }

          .bracket-round {
            min-width: auto;
          }

          .participants-grid {
            grid-template-columns: 1fr;
            gap: 10px;
          }

          .vs-text {
            order: 2;
          }

          .modal-content {
            width: 95%;
            margin: 20px;
          }
        }
      `}</style>
    </div>
  );
};

export default TournamentBracket;