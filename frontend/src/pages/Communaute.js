import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Communaute = () => {
  const { API_BASE_URL } = useAuth();
  const [activeView, setActiveView] = useState('membres');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // State for real data from API
  const [communityStats, setCommunityStats] = useState({});
  const [members, setMembers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  // Filtered data based on search
  const filteredMembers = members.filter(member => 
    member.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (member.profile?.display_name && member.profile.display_name.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const filteredTeams = teams.filter(team =>
    team.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    team.captain.toLowerCase().includes(searchTerm.toLowerCase()) ||
    team.members.some(member => member.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  useEffect(() => {
    fetchCommunityData();
  }, []);

  const fetchCommunityData = async () => {
    setLoading(true);
    try {
      // Fetch community statistics
      const statsResponse = await fetch(`${API_BASE_URL}/community/stats`);
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setCommunityStats(statsData);
      }

      // Fetch community members
      const membersResponse = await fetch(`${API_BASE_URL}/community/members`);
      if (membersResponse.ok) {
        const membersData = await membersResponse.json();
        setMembers(membersData.members || []);
      }

      // Fetch community teams
      const teamsResponse = await fetch(`${API_BASE_URL}/community/teams`);
      if (teamsResponse.ok) {
        const teamsData = await teamsResponse.json();
        setTeams(teamsData.teams || []);
      }

      // Fetch leaderboard
      const leaderboardResponse = await fetch(`${API_BASE_URL}/community/leaderboard`);
      if (leaderboardResponse.ok) {
        const leaderboardData = await leaderboardResponse.json();
        setLeaderboard(leaderboardData.leaderboard || []);
      }

    } catch (error) {
      console.error('Erreur lors du chargement des données communautaires:', error);
      setError('Erreur lors du chargement des données communautaires');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'status-online';
      case 'inactive': return 'status-away';
      default: return 'status-offline';
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'admin': return 'role-admin';
      case 'moderator': return 'role-moderator';
      case 'member': return 'role-member';
      default: return 'role-member';
    }
  };

  const getRoleDisplay = (role) => {
    switch (role) {
      case 'admin': return 'Admin';
      case 'moderator': return 'Modérateur';
      case 'member': return 'Membre';
      default: return 'Membre';
    }
  };

  const getGameDisplay = (game) => {
    switch (game) {
      case 'cs2': return 'Counter-Strike 2';
      case 'lol': return 'League of Legends';
      case 'wow': return 'World of Warcraft';
      case 'sc2': return 'StarCraft II';
      case 'minecraft': return 'Minecraft';
      default: return game;
    }
  };

  if (loading) {
    return (
      <div className="page-pro">
        <div className="container-pro">
          <div className="loading">Chargement des données communautaires...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-pro">
        <div className="container-pro">
          <div className="error">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-pro">
      {/* Header */}
      <section className="page-header-pro community-header">
        <div className="community-bg">
          <div className="community-overlay"></div>
          <div className="community-pattern"></div>
        </div>
        <div className="container-pro">
          <div className="community-badge">
            <svg className="community-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12C14.21 12 16 10.21 16 8S14.21 4 12 4 8 5.79 8 8 9.79 12 12 12M12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z"/>
            </svg>
            <span>COMMUNAUTÉ ÉLITE</span>
          </div>
          <h1 className="page-title-pro community-title">COMMUNAUTÉ</h1>
          <p className="page-subtitle-pro">
            Découvrez les membres, équipes et champions de la Oupafamilly
          </p>
        </div>
      </section>

      {/* Community Stats */}
      <section className="section-pro">
        <div className="container-pro">
          <div className="community-stats-pro">
            <div className="stat-card-pro">
              <div className="stat-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12C14.21 12 16 10.21 16 8S14.21 4 12 4 8 5.79 8 8 9.79 12 12 12M12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z"/>
                </svg>
              </div>
              <div className="stat-content">
                <div className="stat-number">{communityStats.users?.total || 0}</div>
                <div className="stat-label">Membres inscrits</div>
              </div>
            </div>
            <div className="stat-card-pro">
              <div className="stat-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M16 4C16.88 4 17.67 4.5 18 5.26L20 9H16L15 7H9L8 9H4L6 5.26C6.33 4.5 7.12 4 8 4H16M4 10H20V16H18V14H16V16H8V14H6V16H4V10Z"/>
                </svg>
              </div>
              <div className="stat-content">
                <div className="stat-number">{communityStats.teams?.total || 0}</div>
                <div className="stat-label">Équipes actives</div>
              </div>
            </div>
            <div className="stat-card-pro">
              <div className="stat-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M5 16L3 5H1V3H4L6 14H18.5L21 6H8L8.25 5H22L19 17H6L5 16Z"/>
                </svg>
              </div>
              <div className="stat-content">
                <div className="stat-number">{communityStats.users?.active_last_week || 0}</div>
                <div className="stat-label">Actifs cette semaine</div>
              </div>
            </div>
            <div className="stat-card-pro">
              <div className="stat-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L15.09 8.26L22 9L16 14.74L17.18 21.02L12 18.77L6.82 21.02L8 14.74L2 9L8.91 8.26L12 2Z"/>
                </svg>
              </div>
              <div className="stat-content">
                <div className="stat-number">{communityStats.tournaments?.completed || 0}</div>
                <div className="stat-label">Tournois terminés</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* View Tabs */}
      <section className="section-pro section-alt-pro">
        <div className="container-pro">
          <div className="community-tabs-pro">
            <button
              className={`community-tab-pro ${activeView === 'membres' ? 'active' : ''}`}
              onClick={() => setActiveView('membres')}
            >
              <span>MEMBRES</span>
            </button>
            <button
              className={`community-tab-pro ${activeView === 'equipes' ? 'active' : ''}`}
              onClick={() => setActiveView('equipes')}
            >
              <span>ÉQUIPES</span>
            </button>
            <button
              className={`community-tab-pro ${activeView === 'classement' ? 'active' : ''}`}
              onClick={() => setActiveView('classement')}
            >
              <span>CLASSEMENT</span>
            </button>
          </div>

          {/* Search Bar */}
          {(activeView === 'membres' || activeView === 'equipes') && (
            <div className="search-section">
              <div className="search-container">
                <div className="search-icon">🔍</div>
                <input
                  type="text"
                  placeholder={`Rechercher ${activeView === 'membres' ? 'un membre' : 'une équipe'}...`}
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="search-input"
                />
                {searchTerm && (
                  <button
                    className="search-clear"
                    onClick={() => setSearchTerm('')}
                    title="Effacer la recherche"
                  >
                    ×
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Members View */}
          {activeView === 'membres' && (
            <div className="members-grid-pro">
              {filteredMembers.length === 0 ? (
                <div className="no-results">
                  <p>
                    {searchTerm 
                      ? `Aucun membre trouvé pour "${searchTerm}"` 
                      : 'Aucun membre pour le moment'
                    }
                  </p>
                </div>
              ) : (
                filteredMembers.map(member => (
                  <div key={member.id} className="member-card-pro">
                    <div className="member-header-pro">
                    <div className="member-avatar-pro">
                      {member.profile?.avatar_url ? (
                        <img 
                          src={member.profile.avatar_url} 
                          alt={member.username}
                          className="avatar-image"
                        />
                      ) : (
                        <svg viewBox="0 0 24 24" fill="currentColor">
                          <path d="M12 12C14.21 12 16 10.21 16 8S14.21 4 12 4 8 5.79 8 8 9.79 12 12 12M12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z"/>
                        </svg>
                      )}
                    </div>
                    <div className="member-info-pro">
                      <h3 className="member-name-pro">{member.profile?.display_name || member.username}</h3>
                      <p className="member-pseudo-pro">@{member.username}</p>
                    </div>
                    <span className={`member-status-pro ${getStatusColor(member.status)}`}>
                      {member.status === 'active' ? 'En ligne' : 'Hors ligne'}
                    </span>
                  </div>

                  <div className="member-details-pro">
                    <div className="member-role-pro">
                      <span className={`role-badge-pro ${getRoleColor(member.role)}`}>
                        {getRoleDisplay(member.role)}
                      </span>
                    </div>
                    
                    <div className="member-stats-pro">
                      <div className="member-stat">
                        <span className="stat-label">Trophées</span>
                        <span className="stat-value">{member.trophies?.total || 0}</span>
                      </div>
                      <div className="member-stat">
                        <span className="stat-label">1v1</span>
                        <span className="stat-value trophy-1v1">{member.trophies?.['1v1'] || 0}</span>
                      </div>
                      <div className="member-stat">
                        <span className="stat-label">2v2</span>
                        <span className="stat-value trophy-2v2">{member.trophies?.['2v2'] || 0}</span>
                      </div>
                      <div className="member-stat">
                        <span className="stat-label">5v5</span>
                        <span className="stat-value trophy-5v5">{member.trophies?.['5v5'] || 0}</span>
                      </div>
                    </div>

                    {member.profile?.favorite_games && member.profile.favorite_games.length > 0 && (
                      <div className="member-games-pro">
                        <span className="games-label">Spécialités :</span>
                        <div className="games-list-pro">
                          {member.profile.favorite_games.map(game => (
                            <span key={game} className="game-tag-pro">{getGameDisplay(game)}</span>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="member-join-pro">
                      Membre depuis {new Date(member.created_at).toLocaleDateString('fr-FR', { 
                        year: 'numeric', 
                        month: 'long' 
                      })}
                    </div>
                  </div>

                  <div className="member-actions-pro">
                    <Link 
                      to={`/profil/${member.id}`} 
                      className="btn-outline-pro btn-sm"
                    >
                      PROFIL
                    </Link>
                  </div>
                </div>
              ))
              )}
            </div>
          )}

          {/* Teams View */}
          {activeView === 'equipes' && (
            <div className="teams-grid-pro">
              {filteredTeams.length === 0 ? (
                <div className="no-results">
                  <p>
                    {searchTerm 
                      ? `Aucune équipe trouvée pour "${searchTerm}"` 
                      : 'Aucune équipe pour le moment'
                    }
                  </p>
                </div>
              ) : (
                filteredTeams.map(team => (
                <div key={team.id} className="team-card-pro">
                  <div className="team-header-pro">
                    <div className="team-icon-pro">
                      <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M16 4C16.88 4 17.67 4.5 18 5.26L20 9H16L15 7H9L8 9H4L6 5.26C6.33 4.5 7.12 4 8 4H16M4 10H20V16H18V14H16V16H8V14H6V16H4V10Z"/>
                      </svg>
                    </div>
                    <div className="team-info-pro">
                      <h3 className="team-name-pro">{team.name}</h3>
                      <p className="team-game-pro">{getGameDisplay(team.game)}</p>
                    </div>
                    <div className="team-rank-badge">
                      <span className="rank-number">#{team.rank}</span>
                    </div>
                  </div>

                  <div className="team-stats-pro">
                    <div className="team-stat-item">
                      <span className="stat-label">Tournois</span>
                      <span className="stat-value">{team.statistics?.total_tournaments || 0}</span>
                    </div>
                    <div className="team-stat-item">
                      <span className="stat-label">Victoires</span>
                      <span className="stat-value win">{team.statistics?.tournaments_won || 0}</span>
                    </div>
                    <div className="team-stat-item">
                      <span className="stat-label">Winrate</span>
                      <span className="stat-value winrate">{team.statistics?.win_rate || 0}%</span>
                    </div>
                    <div className="team-stat-item">
                      <span className="stat-label">Points</span>
                      <span className="stat-value points">{team.statistics?.total_points || 0}</span>
                    </div>
                  </div>

                  <div className="team-members-pro">
                    <h4 className="members-title-pro">Roster ({team.member_count}/{team.max_members})</h4>
                    <div className="members-list-pro">
                      <div className="captain-member">
                        <span className="captain-icon">👑</span>
                        <span className="member-name">{team.captain}</span>
                      </div>
                      {team.members.filter(member => member !== team.captain).map(memberName => (
                        <span key={memberName} className="member-tag-pro">
                          {memberName}
                        </span>
                      ))}
                    </div>
                    {team.is_open && team.member_count < team.max_members && (
                      <div className="team-recruiting">
                        <span className="recruiting-badge">🔍 Recrute</span>
                        <span className="spots-available">{team.max_members - team.member_count} places disponibles</span>
                      </div>
                    )}
                  </div>

                  {team.statistics?.victories_by_type && (
                    <div className="team-trophies-pro">
                      <h4 className="trophies-title-pro">Trophées par mode</h4>
                      <div className="trophies-breakdown">
                        <div className="trophy-item">
                          <span className="trophy-label">1v1</span>
                          <span className="trophy-count">{team.statistics.victories_by_type['1v1'] || 0}</span>
                        </div>
                        <div className="trophy-item">
                          <span className="trophy-label">2v2</span>
                          <span className="trophy-count">{team.statistics.victories_by_type['2v2'] || 0}</span>
                        </div>
                        <div className="trophy-item">
                          <span className="trophy-label">5v5</span>
                          <span className="trophy-count">{team.statistics.victories_by_type['5v5'] || 0}</span>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="team-actions-pro">
                    <button className="btn-primary-pro btn-team">VOIR L'ÉQUIPE</button>
                    {team.is_open && team.member_count < team.max_members && (
                      <button className="btn-secondary-pro btn-team">REJOINDRE</button>
                    )}
                  </div>
                </div>
              ))
              )}
            </div>
          )}

          {/* Leaderboard View */}
          {activeView === 'classement' && (
            <div className="leaderboard-pro">
              <div className="leaderboard-header-pro">
                <h2 className="leaderboard-title-pro">Hall of Fame</h2>
                <p className="leaderboard-subtitle-pro">Les légendes de la Oupafamilly</p>
                <div className="leaderboard-legend">
                  <div className="legend-item">
                    <span className="trophy-icon-1v1">🏆</span>
                    <span>1v1: 100 pts</span>
                  </div>
                  <div className="legend-item">
                    <span className="trophy-icon-2v2">🥇</span>
                    <span>2v2: 150 pts</span>
                  </div>
                  <div className="legend-item">
                    <span className="trophy-icon-5v5">🏅</span>
                    <span>5v5: 200 pts</span>
                  </div>
                </div>
              </div>

              <div className="leaderboard-list-pro">
                {leaderboard.map(player => (
                  <div key={player.rank} className={`leaderboard-item-pro ${player.rank <= 3 ? 'podium' : ''}`}>
                    <div className="rank-badge-pro">
                      {player.rank <= 3 ? (
                        <span className="trophy-pro">
                          {player.rank === 1 ? (
                            <svg className="trophy-gold" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M12 2L15.09 8.26L22 9L16 14.74L17.18 21.02L12 18.77L6.82 21.02L8 14.74L2 9L8.91 8.26L12 2Z"/>
                            </svg>
                          ) : player.rank === 2 ? (
                            <svg className="trophy-silver" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M12 2L15.09 8.26L22 9L16 14.74L17.18 21.02L12 18.77L6.82 21.02L8 14.74L2 9L8.91 8.26L12 2Z"/>
                            </svg>
                          ) : (
                            <svg className="trophy-bronze" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M12 2L15.09 8.26L22 9L16 14.74L17.18 21.02L12 18.77L6.82 21.02L8 14.74L2 9L8.91 8.26L12 2Z"/>
                            </svg>
                          )}
                        </span>
                      ) : (
                        <span className="rank-number-pro">#{player.rank}</span>
                      )}
                    </div>
                    
                    <div className="player-info-pro">
                      <h3 className="player-name-pro">{player.username}</h3>
                      <div className="player-stats-pro">
                        <span className="points-pro">{player.total_points} points</span>
                        <div className="trophies-breakdown-inline">
                          <span className="trophy-detail">
                            <span className="trophy-icon-1v1">🏆</span>
                            {player.victories_1v1}
                          </span>
                          <span className="trophy-detail">
                            <span className="trophy-icon-2v2">🥇</span>
                            {player.victories_2v2}
                          </span>
                          <span className="trophy-detail">
                            <span className="trophy-icon-5v5">🏅</span>
                            {player.victories_5v5}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="player-badge-pro">
                      <span className={`champion-badge-pro rank-${player.rank}`}>
                        {player.badge}
                      </span>
                      <div className="total-trophies">
                        <svg className="trophy-icon-small" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M12 2L15.09 8.26L22 9L16 14.74L17.18 21.02L12 18.77L6.82 21.02L8 14.74L2 9L8.91 8.26L12 2Z"/>
                        </svg>
                        {player.total_trophies}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Join CTA */}
      <section className="cta-section-pro">
        <div className="cta-bg">
          <div className="cta-pattern"></div>
        </div>
        <div className="container-pro">
          <div className="cta-content-pro">
            <div className="cta-badge">
              <span>REJOIGNEZ-NOUS</span>
            </div>
            <h2 className="cta-title-pro">Prêt à intégrer l'élite ?</h2>
            <p className="cta-subtitle-pro">
              Rejoignez une communauté d'exception où talent et passion se rencontrent
            </p>
            <div className="cta-buttons-pro">
              <button 
                className="btn-primary-pro btn-large"
                onClick={() => {
                  // Emit custom event to open auth modal
                  window.dispatchEvent(new CustomEvent('openAuthModal', { detail: { mode: 'register' } }));
                }}
              >
                <span>NOUS REJOINDRE</span>
                <svg className="btn-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Communaute;