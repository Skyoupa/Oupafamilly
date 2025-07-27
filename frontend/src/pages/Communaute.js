import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Inventaire from '../components/Inventaire';

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
  
  // New community features state
  const [userProfile, setUserProfile] = useState({ coins: 0, level: 1, experience_points: 0 });
  const [marketplaceItems, setMarketplaceItems] = useState([]);
  const [bettingMarkets, setBettingMarkets] = useState([]);
  const [userBets, setUserBets] = useState([]);
  const [messages, setMessages] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showInventory, setShowInventory] = useState(false);
  
  // Messaging state
  const [memberSearch, setMemberSearch] = useState('');
  const [selectedRecipient, setSelectedRecipient] = useState('');
  const [messageContent, setMessageContent] = useState('');
  
  // Team management state
  const [showCreateTeamModal, setShowCreateTeamModal] = useState(false);
  const [showManageTeamModal, setShowManageTeamModal] = useState(false);
  const [selectedTeamForManagement, setSelectedTeamForManagement] = useState(null);
  const [userTeams, setUserTeams] = useState([]);
  const [teamForm, setTeamForm] = useState({
    name: '',
    game: 'cs2',
    description: '',
    max_members: 5,
    is_open: true
  });
  const [teamLoading, setTeamLoading] = useState(false);
  
  // Tournament scheduling state
  const [tournaments, setTournaments] = useState([]);
  const [selectedTournament, setSelectedTournament] = useState('');
  const [tournamentSchedule, setTournamentSchedule] = useState(null);
  const [upcomingMatches, setUpcomingMatches] = useState([]);
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [scheduleForm, setScheduleForm] = useState({
    date: '',
    time: '',
    notes: ''
  });

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
    fetchUserProfile();
    fetchCommunityFeatures();
    fetchTournamentData();
    if (localStorage.getItem('token')) {
      fetchUserTeams();
    }
  }, []);

  const fetchUserTeams = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/teams/my-teams`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setUserTeams(data.teams || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des équipes:', error);
    }
  };

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

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/currency/balance`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setUserProfile(data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement du profil:', error);
    }
  };

  const fetchCommunityFeatures = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

      // Fetch marketplace items with enhanced debugging (no auth required)
      console.log('Fetching marketplace items...');
      console.log('API URL:', `${API_BASE_URL}/currency/marketplace`);
      console.log('Headers:', headers);
      
      const marketResponse = await fetch(`${API_BASE_URL}/currency/marketplace`);
      console.log('Marketplace response status:', marketResponse.status);
      console.log('Marketplace response ok:', marketResponse.ok);
      
      if (marketResponse.ok) {
        const marketData = await marketResponse.json();
        console.log('Marketplace data received:', marketData);
        console.log('Number of items:', marketData.length);
        setMarketplaceItems(marketData.slice(0, 4)); // Show only 4 items
      } else {
        const errorText = await marketResponse.text();
        console.error('Failed to fetch marketplace items:', marketResponse.status, marketResponse.statusText);
        console.error('Error response:', errorText);
      }

      // Only fetch authenticated endpoints if we have a token
      if (token) {
        const authHeaders = { 'Authorization': `Bearer ${token}` };
        
        // Fetch betting markets
        const bettingResponse = await fetch(`${API_BASE_URL}/betting/markets?status=open`, { headers: authHeaders });
        if (bettingResponse.ok) {
          const bettingData = await bettingResponse.json();
          setBettingMarkets(bettingData.slice(0, 3)); // Show only 3 markets
        }

        // Fetch user bets
        const userBetsResponse = await fetch(`${API_BASE_URL}/betting/bets/my-bets?limit=3`, { headers: authHeaders });
        if (userBetsResponse.ok) {
          const userBetsData = await userBetsResponse.json();
          setUserBets(userBetsData);
        }
        
        // Fetch messages
        const messagesResponse = await fetch(`${API_BASE_URL}/chat/private?limit=5`, { headers: authHeaders });
        if (messagesResponse.ok) {
          const messagesData = await messagesResponse.json();
          setMessages(messagesData);
        }

        // Fetch unread count
        const unreadResponse = await fetch(`${API_BASE_URL}/chat/private/unread-count`, { headers: authHeaders });
        if (unreadResponse.ok) {
          const unreadData = await unreadResponse.json();
          setUnreadCount(unreadData.unread_count);
        }
      }
    } catch (error) {
      console.error('Erreur lors du chargement des fonctionnalités communautaires:', error);
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

  // Tournament scheduling functions
  const fetchTournamentData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
      
      // Fetch tournaments from correct API (public endpoint)
      console.log('Fetching tournaments...');
      const tournamentsResponse = await fetch(`${API_BASE_URL}/tournaments/`, { headers });
      console.log('Tournaments response status:', tournamentsResponse.status);
      
      if (tournamentsResponse.ok) {
        const tournamentsData = await tournamentsResponse.json();
        console.log('Tournaments data:', tournamentsData);
        setTournaments(tournamentsData);
      } else {
        console.error('Erreur lors de la récupération des tournois:', tournamentsResponse.status);
      }

      // Fetch upcoming matches (requires auth)
      if (token) {
        const upcomingResponse = await fetch(`${API_BASE_URL}/match-scheduling/upcoming-matches?days=7&limit=10`, { 
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (upcomingResponse.ok) {
          const upcomingData = await upcomingResponse.json();
          setUpcomingMatches(upcomingData);
        } else {
          console.error('Erreur lors de la récupération des matchs à venir:', upcomingResponse.status);
        }
      }
    } catch (error) {
      console.error('Erreur lors du chargement des tournois:', error);
    }
  };

  const fetchTournamentSchedule = async (tournamentId) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const headers = { 'Authorization': `Bearer ${token}` };
      const response = await fetch(`${API_BASE_URL}/match-scheduling/tournament/${tournamentId}/matches`, { headers });
      
      if (response.ok) {
        const data = await response.json();
        setTournamentSchedule(data);
      } else {
        console.error('Erreur lors de la récupération du planning du tournoi');
        setError('Erreur lors de la récupération du planning du tournoi');
      }
    } catch (error) {
      console.error('Erreur lors de la récupération du planning:', error);
      setError('Erreur lors de la récupération du planning');
    }
  };

  const scheduleMatch = async (matchId, scheduledTime, notes = '') => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const headers = { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };

      const response = await fetch(`${API_BASE_URL}/match-scheduling/schedule-match`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          match_id: matchId,
          scheduled_time: scheduledTime,
          notes
        })
      });

      if (response.ok) {
        // Refresh tournament schedule
        if (selectedTournament) {
          await fetchTournamentSchedule(selectedTournament);
        }
        await fetchTournamentData(); // Refresh upcoming matches
        return true;
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la programmation du match');
        return false;
      }
    } catch (error) {
      console.error('Erreur lors de la programmation du match:', error);
      setError('Erreur lors de la programmation du match');
      return false;
    }
  };

  const handleScheduleMatch = (match) => {
    setSelectedMatch(match);
    
    // Initialize form with current schedule if exists
    if (match.scheduled_time) {
      const scheduledDate = new Date(match.scheduled_time);
      setScheduleForm({
        date: scheduledDate.toISOString().split('T')[0],
        time: scheduledDate.toTimeString().slice(0, 5),
        notes: match.notes || ''
      });
    } else {
      // Default to tomorrow at 18:00
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      tomorrow.setHours(18, 0, 0, 0);
      
      setScheduleForm({
        date: tomorrow.toISOString().split('T')[0],
        time: '18:00',
        notes: ''
      });
    }
    
    setShowScheduleModal(true);
  };

  const submitSchedule = async () => {
    if (!selectedMatch || !scheduleForm.date || !scheduleForm.time) return;

    // Combine date and time into ISO string using local timezone
    const localDateTime = new Date(`${scheduleForm.date}T${scheduleForm.time}`);
    const scheduledTime = localDateTime.toISOString();

    const success = await scheduleMatch(selectedMatch.id, scheduledTime, scheduleForm.notes);
    
    if (success) {
      setShowScheduleModal(false);
      setSelectedMatch(null);
      setScheduleForm({ date: '', time: '', notes: '' });
    }
  };

  const formatDateTime = (dateTime) => {
    if (!dateTime) return 'Non programmé';
    
    const date = new Date(dateTime);
    return date.toLocaleString('fr-FR', {
      dateStyle: 'short',
      timeStyle: 'short'
    });
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

  const handleDailyBonus = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/currency/daily-bonus`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      const data = await response.json();
      if (response.ok) {
        alert(`Bonus réclamé ! +${data.bonus_amount} coins`);
        fetchUserProfile();
      } else {
        alert(data.detail || 'Erreur');
      }
    } catch (error) {
      console.error('Erreur bonus quotidien:', error);
    }
  };

  const buyMarketplaceItem = async (itemId, itemName, price) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/currency/marketplace/buy/${itemId}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      const data = await response.json();
      if (response.ok) {
        alert(`Achat réussi ! ${itemName} ajouté à votre inventaire`);
        fetchUserProfile();
        fetchCommunityFeatures();
      } else {
        alert(data.detail || 'Erreur lors de l\'achat');
      }
    } catch (error) {
      console.error('Erreur achat:', error);
    }
  };

  const placeBet = async (marketId, optionId, amount) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/betting/bets`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ market_id: marketId, option_id: optionId, amount })
      });

      const data = await response.json();
      if (response.ok) {
        alert(`Pari placé avec succès ! ${amount} coins misés`);
        fetchUserProfile();
        fetchCommunityFeatures();
      } else {
        alert(data.detail || 'Erreur lors du pari');
      }
    } catch (error) {
      console.error('Erreur pari:', error);
    }
  };

  const sendMessage = async (recipientId, content) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/chat/private`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ recipient_id: recipientId, content })
      });

      if (response.ok) {
        alert('Message envoyé !');
        setMessageContent('');
        setSelectedRecipient('');
        fetchCommunityFeatures();
      }
    } catch (error) {
      console.error('Erreur envoi message:', error);
    }
  };

  const handleSendMessage = () => {
    if (selectedRecipient && messageContent.trim()) {
      sendMessage(selectedRecipient, messageContent);
    }
  };

  const filteredMembersForMessaging = members.filter(member => 
    (member.profile?.display_name || member.username)
      .toLowerCase()
      .includes(memberSearch.toLowerCase())
  );

  // Fonctions de gestion des équipes
  const createTeam = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      alert('Vous devez être connecté pour créer une équipe');
      return;
    }

    setTeamLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/teams/create`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(teamForm)
      });

      const data = await response.json();
      if (response.ok) {
        alert('Équipe créée avec succès !');
        setShowCreateTeamModal(false);
        setTeamForm({
          name: '',
          game: 'cs2',
          description: '',
          max_members: 5,
          is_open: true
        });
        fetchCommunityData();
        fetchUserTeams();
      } else {
        alert(data.detail || 'Erreur lors de la création de l\'équipe');
      }
    } catch (error) {
      console.error('Erreur création équipe:', error);
      alert('Erreur de connexion au serveur');
    } finally {
      setTeamLoading(false);
    }
  };

  const deleteTeam = async (teamId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette équipe ?')) {
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch(`${API_BASE_URL}/teams/${teamId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert('Équipe supprimée avec succès !');
        setShowManageTeamModal(false);
        fetchCommunityData();
        fetchUserTeams();
      } else {
        const data = await response.json();
        alert(data.detail || 'Erreur lors de la suppression');
      }
    } catch (error) {
      console.error('Erreur suppression équipe:', error);
      alert('Erreur de connexion au serveur');
    }
  };

  const leaveTeam = async (teamId) => {
    if (!confirm('Êtes-vous sûr de vouloir quitter cette équipe ?')) {
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch(`${API_BASE_URL}/teams/${teamId}/leave`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert('Vous avez quitté l\'équipe avec succès !');
        setShowManageTeamModal(false);
        fetchCommunityData();
        fetchUserTeams();
      } else {
        const data = await response.json();
        alert(data.detail || 'Erreur lors de la sortie d\'équipe');
      }
    } catch (error) {
      console.error('Erreur sortie équipe:', error);
      alert('Erreur de connexion au serveur');
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
          
          {/* User Status Bar */}
          <div className="user-status-bar">
            <div className="status-item">
              <span className="status-icon">💰</span>
              <span className="status-value">{userProfile.balance || 0}</span>
              <span className="status-label">Coins</span>
            </div>
            <div className="status-item">
              <span className="status-icon">⭐</span>
              <span className="status-value">Niv. {userProfile.level || 1}</span>
              <span className="status-label">Niveau</span>
            </div>
            <div className="status-item">
              <span className="status-icon">📧</span>
              <span className="status-value">{unreadCount}</span>
              <span className="status-label">Messages</span>
            </div>
          </div>
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
            <button
              className={`community-tab-pro ${activeView === 'tournois' ? 'active' : ''}`}
              onClick={() => {
                setActiveView('tournois');
                fetchTournamentData();
              }}
            >
              <span>🏆 TOURNOIS</span>
            </button>
            <button
              className={`community-tab-pro ${activeView === 'marketplace' ? 'active' : ''}`}
              onClick={() => setActiveView('marketplace')}
            >
              <span>🛒 MARKETPLACE</span>
            </button>
            <button
              className={`community-tab-pro ${activeView === 'paris' ? 'active' : ''}`}
              onClick={() => setActiveView('paris')}
            >
              <span>🎲 PARIS</span>
            </button>
            <button
              className={`community-tab-pro ${activeView === 'messagerie' ? 'active' : ''}`}
              onClick={() => setActiveView('messagerie')}
            >
              <span>📧 MESSAGERIE {unreadCount > 0 && <span className="unread-badge">{unreadCount}</span>}</span>
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
            <div>
              {/* Team Management Header */}
              <div className="teams-management-header">
                <div className="teams-header-content">
                  <h3>⚔️ Gestion des Équipes</h3>
                  <p>Créez votre équipe ou gérez vos équipes existantes</p>
                </div>
                <div className="teams-actions">
                  <button 
                    className="btn-create-team"
                    onClick={() => setShowCreateTeamModal(true)}
                  >
                    ➕ Créer une équipe
                  </button>
                  {userTeams.length > 0 && (
                    <button 
                      className="btn-manage-teams"
                      onClick={() => setShowManageTeamModal(true)}
                    >
                      ⚙️ Gérer mes équipes ({userTeams.length})
                    </button>
                  )}
                </div>
              </div>

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

          {/* Marketplace View */}
          {activeView === 'marketplace' && (
            <div className="marketplace-section">
              <div className="marketplace-header">
                <h2>🛒 Marketplace Communautaire</h2>
                <p>Utilisez vos coins pour acheter des objets exclusifs</p>
                <button className="btn-primary-pro" onClick={handleDailyBonus}>
                  🎁 Bonus Quotidien
                </button>
                
                <button 
                  className="btn-secondary-pro inventory-btn"
                  onClick={() => setShowInventory(true)}
                >
                  💼 Mon Inventaire
                </button>
              </div>
              
              <div className="marketplace-grid">
                {marketplaceItems.length === 0 ? (
                  <div className="no-items-message">
                    <p>Aucun article disponible pour le moment. Veuillez réessayer plus tard.</p>
                    <button 
                      className="btn-secondary-pro"
                      onClick={() => window.location.reload()}
                    >
                      🔄 Actualiser
                    </button>
                  </div>
                ) : (
                  marketplaceItems.map(item => (
                    <div key={item.id} className="marketplace-item">
                      {/* Visuel de l'item */}
                      <div className={`item-visual item-visual-${item.item_type}`}>
                        {item.item_type === 'avatar' && (
                          <div className="avatar-preview">
                            <div className="avatar-icon">👤</div>
                            <div className="avatar-effects">✨</div>
                          </div>
                        )}
                        {item.item_type === 'badge' && (
                          <div className="badge-preview">
                            <div className="badge-icon">🏆</div>
                            <div className="badge-text">{item.custom_data?.text || 'BADGE'}</div>
                          </div>
                        )}
                        {item.item_type === 'custom_tag' && (
                          <div 
                            className="tag-preview"
                            style={{
                              background: item.custom_data?.background || 'linear-gradient(135deg, #667eea, #764ba2)',
                              border: item.custom_data?.border || '2px solid #4c51bf',
                              color: item.custom_data?.text_color || '#ffffff'
                            }}
                          >
                            <span>MEMBRE</span>
                          </div>
                        )}
                        {item.item_type === 'title' && (
                          <div className="title-preview">
                            <div className="title-icon">👑</div>
                            <div 
                              className="title-text"
                              style={{color: item.custom_data?.title_color || '#6c5ce7'}}
                            >
                              {item.custom_data?.title_text || 'Titre'}
                            </div>
                          </div>
                        )}
                        {item.item_type === 'theme' && (
                          <div className="theme-preview">
                            <div className="theme-icon">🎨</div>
                            <div className="theme-name">{item.name.replace('Thème Profil ', '')}</div>
                          </div>
                        )}
                        {(item.item_type === 'banner' || item.item_type === 'emote') && (
                          <div className="generic-preview">
                            <div className="generic-icon">
                              {item.item_type === 'banner' ? '🖼️' : '😊'}
                            </div>
                            <div className="generic-text">{item.item_type.toUpperCase()}</div>
                          </div>
                        )}
                      </div>
                      
                      <div className="item-header">
                        <h3>{item.name}</h3>
                        {item.is_premium && <span className="premium-badge">⭐ Premium</span>}
                        {item.rarity && item.rarity !== 'common' && (
                          <span className={`rarity-badge rarity-${item.rarity}`}>
                            {item.rarity.toUpperCase()}
                          </span>
                        )}
                      </div>
                      <p className="item-description">{item.description}</p>
                      <div className="item-type-badge">
                        <span>📦 {item.item_type}</span>
                      </div>
                      <div className="item-footer">
                        <span className="item-price">💰 {item.price} coins</span>
                        <button 
                          className="btn-secondary-pro"
                          onClick={() => buyMarketplaceItem(item.id, item.name, item.price)}
                        >
                          Acheter
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* Betting View */}
          {activeView === 'paris' && (
            <div className="betting-section">
              <div className="betting-header">
                <h2>🎲 Paris Communautaires</h2>
                <p>Pariez vos coins sur les événements de la communauté</p>
              </div>
              
              <div className="betting-markets">
                {bettingMarkets.map(market => (
                  <div key={market.id} className="betting-market">
                    <h3>{market.title}</h3>
                    <p>{market.description}</p>
                    <div className="market-info">
                      <span>🎮 {market.game.toUpperCase()}</span>
                      <span>💰 Pool: {market.total_pool} coins</span>
                      <span>📅 Ferme: {new Date(market.closes_at).toLocaleDateString()}</span>
                    </div>
                    <div className="betting-options">
                      {market.options.map(option => (
                        <div key={option.option_id} className="betting-option">
                          <span className="option-name">{option.name}</span>
                          <span className="option-odds">Cote: {option.odds}x</span>
                          <button 
                            className="btn-outline-pro"
                            onClick={() => {
                              const amount = prompt('Montant à parier (coins):');
                              if (amount && !isNaN(amount) && amount > 0) {
                                placeBet(market.id, option.option_id, parseInt(amount));
                              }
                            }}
                          >
                            Parier
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
              
              {userBets.length > 0 && (
                <div className="user-bets">
                  <h3>Mes Paris Récents</h3>
                  {userBets.map(bet => (
                    <div key={bet.id} className="bet-item">
                      <span>{bet.option_name}</span>
                      <span>{bet.amount} coins</span>
                      <span className={`bet-status ${bet.status}`}>
                        {bet.status === 'active' ? 'En cours' : bet.status === 'won' ? 'Gagné' : 'Perdu'}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Messaging View */}
          {activeView === 'messagerie' && (
            <div className="messaging-section-modern">
              <div className="messaging-header-modern">
                <h2>📧 Messagerie Privée</h2>
                <p>Communiquez directement avec les membres de la communauté</p>
              </div>
              
              <div className="messaging-layout">
                {/* Left Panel - Member List */}
                <div className="member-list-panel">
                  <div className="member-search-box">
                    <input
                      type="text"
                      placeholder="🔍 Rechercher un membre..."
                      value={memberSearch}
                      onChange={(e) => setMemberSearch(e.target.value)}
                      className="search-input-modern"
                    />
                  </div>
                  
                  <div className="members-scroll-list">
                    <h4>Membres disponibles ({filteredMembersForMessaging.length})</h4>
                    {filteredMembersForMessaging.map(member => (
                      <div 
                        key={member.id} 
                        className={`member-item-selectable ${selectedRecipient === member.id ? 'selected' : ''}`}
                        onClick={() => setSelectedRecipient(member.id)}
                      >
                        <div className="member-avatar">
                          {(member.profile?.display_name || member.username).charAt(0).toUpperCase()}
                        </div>
                        <div className="member-info">
                          <span className="member-name">
                            {member.profile?.display_name || member.username}
                          </span>
                          <span className="member-level">
                            Niveau {member.profile?.level || 1}
                          </span>
                        </div>
                      </div>
                    ))}
                    
                    {filteredMembersForMessaging.length === 0 && (
                      <div className="no-members-found">
                        <p>Aucun membre trouvé</p>
                      </div>
                    )}
                  </div>
                </div>
                
                {/* Right Panel - Conversation */}
                <div className="conversation-panel">
                  {selectedRecipient ? (
                    <>
                      <div className="conversation-header">
                        <h4>💬 Conversation avec {
                          filteredMembersForMessaging.find(m => m.id === selectedRecipient)?.profile?.display_name ||
                          filteredMembersForMessaging.find(m => m.id === selectedRecipient)?.username ||
                          'Membre'
                        }</h4>
                      </div>
                      
                      <div className="message-composer">
                        <textarea
                          value={messageContent}
                          onChange={(e) => setMessageContent(e.target.value)}
                          placeholder="Tapez votre message ici..."
                          className="message-textarea-modern"
                          rows="4"
                        />
                        <button 
                          onClick={handleSendMessage}
                          className="send-button-modern"
                          disabled={!messageContent.trim()}
                        >
                          📨 Envoyer Message
                        </button>
                      </div>
                    </>
                  ) : (
                    <div className="no-conversation-selected">
                      <div className="select-member-prompt">
                        <h4>💬 Sélectionnez un membre</h4>
                        <p>Choisissez un membre dans la liste pour commencer une conversation</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
              
              {/* Recent Messages */}
              <div className="recent-messages-modern">
                <h3>📬 Messages Récents</h3>
                <div className="messages-list-modern">
                  {messages.length === 0 ? (
                    <div className="no-messages-modern">
                      <p>💭 Aucun message pour le moment</p>
                      <p>Commencez une conversation en sélectionnant un membre ci-dessus</p>
                    </div>
                  ) : (
                    messages.map(message => (
                      <div key={message.id} className="message-card-modern">
                        <div className="message-header-modern">
                          <div className="message-participants">
                            <span className="message-direction">
                              {message.sender_id === userProfile.user_id ? 
                                '📤 Vous → ' : '📥 De : '
                              }
                            </span>
                            <span className="message-other-party">
                              {message.sender_id === userProfile.user_id ? 'Destinataire' : 'Expéditeur'}
                            </span>
                          </div>
                          <div className="message-meta">
                            <span className="message-date-modern">
                              {new Date(message.created_at).toLocaleDateString('fr-FR')} à{' '}
                              {new Date(message.created_at).toLocaleTimeString('fr-FR', { 
                                hour: '2-digit', 
                                minute: '2-digit' 
                              })}
                            </span>
                            {!message.is_read && message.sender_id !== userProfile.user_id && (
                              <span className="unread-badge-modern">Nouveau</span>
                            )}
                          </div>
                        </div>
                        <div className="message-content-modern">{message.content}</div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Tournament Scheduling View */}
          {activeView === 'tournois' && (
            <div className="tournaments-section">
              <div className="tournaments-header">
                <h2 className="section-title-pro">🏆 Planification des Tournois</h2>
                <p className="section-subtitle-pro">
                  Gérez les horaires des matchs et suivez les tournois en cours
                </p>
              </div>

              {/* Tournament Selector */}
              <div className="tournament-selector-card">
                <div className="selector-header">
                  <h3>📅 Sélectionner un Tournoi</h3>
                  <p>Choisissez un tournoi pour voir et gérer la planification de ses matchs</p>
                </div>
                
                <div className="tournament-select-container">
                  <select 
                    value={selectedTournament} 
                    onChange={(e) => {
                      setSelectedTournament(e.target.value);
                      if (e.target.value) {
                        fetchTournamentSchedule(e.target.value);
                      } else {
                        setTournamentSchedule(null);
                      }
                    }}
                    className="tournament-select"
                  >
                    <option value="">Choisir un tournoi...</option>
                    {tournaments.map(tournament => (
                      <option key={tournament.id} value={tournament.id}>
                        {tournament.title} - {getGameDisplay(tournament.game)} ({tournament.status})
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Tournament Schedule */}
              {tournamentSchedule && (
                <div className="tournament-schedule-card">
                  <div className="schedule-header">
                    <h3>📋 {tournamentSchedule.tournament_name}</h3>
                    <div className="schedule-stats">
                      <span className="stat-item">
                        <strong>{tournamentSchedule.total_matches}</strong> matchs au total
                      </span>
                      <span className="stat-item">
                        <strong>{tournamentSchedule.scheduled_matches}</strong> programmés
                      </span>
                      <span className="stat-item">
                        <strong>{tournamentSchedule.pending_matches}</strong> en attente
                      </span>
                    </div>
                  </div>

                  <div className="matches-grid">
                    {tournamentSchedule.matches.map(match => (
                      <div key={match.id} className={`match-card ${match.scheduled_time ? 'scheduled' : 'pending'}`}>
                        <div className="match-header">
                          <span className="round-badge">R{match.round_number} - M{match.match_number}</span>
                          <span className={`status-badge ${match.status}`}>
                            {match.status === 'scheduled' ? '📅 Programmé' : 
                             match.status === 'in_progress' ? '⚡ En cours' :
                             match.status === 'completed' ? '✅ Terminé' : '⏳ En attente'}
                          </span>
                        </div>

                        <div className="match-players">
                          <div className="player">
                            <span className="player-name">{match.player1_name || 'TBD'}</span>
                          </div>
                          <div className="vs">VS</div>
                          <div className="player">
                            <span className="player-name">{match.player2_name || 'TBD'}</span>
                          </div>
                        </div>

                        <div className="match-schedule-info">
                          <div className="scheduled-time">
                            <span className="time-icon">🕒</span>
                            <span className="time-text">{formatDateTime(match.scheduled_time)}</span>
                          </div>
                          
                          {match.notes && (
                            <div className="match-notes">
                              <span className="notes-icon">📝</span>
                              <span className="notes-text">{match.notes}</span>
                            </div>
                          )}
                        </div>

                        <div className="match-actions">
                          <button 
                            className="btn-schedule"
                            onClick={() => handleScheduleMatch(match)}
                            disabled={match.status === 'completed'}
                          >
                            {match.scheduled_time ? '📝 Modifier' : '📅 Programmer'}
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Upcoming Matches */}
              <div className="upcoming-matches-card">
                <div className="card-header">
                  <h3>🔜 Matchs à Venir</h3>
                  <p>Les prochains matchs programmés dans les 7 jours</p>
                </div>
                
                <div className="upcoming-matches-list">
                  {upcomingMatches.length === 0 ? (
                    <div className="no-matches">
                      <span className="no-matches-icon">📅</span>
                      <p>Aucun match programmé dans les prochains jours</p>
                    </div>
                  ) : (
                    upcomingMatches.map(match => (
                      <div key={match.id} className="upcoming-match-item">
                        <div className="match-datetime">
                          <div className="match-date">{formatDateTime(match.scheduled_time).split(' ')[0]}</div>
                          <div className="match-time">{formatDateTime(match.scheduled_time).split(' ')[1]}</div>
                        </div>
                        
                        <div className="match-details">
                          <div className="match-title">
                            {match.player1_name || 'TBD'} vs {match.player2_name || 'TBD'}
                          </div>
                          <div className="match-tournament">{match.tournament_name}</div>
                          <div className="match-round">Round {match.round_number} - Match {match.match_number}</div>
                        </div>
                        
                        <div className="match-status">
                          <span className={`status-dot ${match.status}`}></span>
                          <span className="status-text">
                            {match.status === 'scheduled' ? 'Programmé' : 
                             match.status === 'in_progress' ? 'En cours' : 'En attente'}
                          </span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Schedule Modal */}
          {showScheduleModal && selectedMatch && (
            <div className="modal-overlay" onClick={() => setShowScheduleModal(false)}>
              <div className="schedule-modal" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                  <h3>📅 Programmer le Match</h3>
                  <button 
                    className="modal-close"
                    onClick={() => setShowScheduleModal(false)}
                  >
                    ✕
                  </button>
                </div>
                
                <div className="modal-content">
                  <div className="match-info">
                    <h4>{selectedMatch.player1_name || 'TBD'} vs {selectedMatch.player2_name || 'TBD'}</h4>
                    <p>Round {selectedMatch.round_number} - Match {selectedMatch.match_number}</p>
                  </div>
                  
                  <div className="schedule-form">
                    <div className="form-group">
                      <label htmlFor="schedule-date">Date du match</label>
                      <input
                        type="date"
                        id="schedule-date"
                        value={scheduleForm.date}
                        onChange={(e) => setScheduleForm({...scheduleForm, date: e.target.value})}
                        min={new Date().toISOString().split('T')[0]}
                        className="form-input"
                      />
                    </div>
                    
                    <div className="form-group">
                      <label htmlFor="schedule-time">Heure du match</label>
                      <input
                        type="time"
                        id="schedule-time"
                        value={scheduleForm.time}
                        onChange={(e) => setScheduleForm({...scheduleForm, time: e.target.value})}
                        className="form-input"
                      />
                    </div>
                    
                    <div className="form-group">
                      <label htmlFor="schedule-notes">Notes (optionnel)</label>
                      <textarea
                        id="schedule-notes"
                        value={scheduleForm.notes}
                        onChange={(e) => setScheduleForm({...scheduleForm, notes: e.target.value})}
                        placeholder="Informations supplémentaires sur le match..."
                        className="form-textarea"
                        rows="3"
                      />
                    </div>
                  </div>
                </div>
                
                <div className="modal-footer">
                  <button 
                    className="btn-cancel"
                    onClick={() => setShowScheduleModal(false)}
                  >
                    Annuler
                  </button>
                  <button 
                    className="btn-confirm"
                    onClick={submitSchedule}
                    disabled={!scheduleForm.date || !scheduleForm.time}
                  >
                    {selectedMatch.scheduled_time ? '✏️ Modifier' : '📅 Programmer'}
                  </button>
                </div>
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
      
      {/* Inventaire Modal */}
      {showInventory && (
        <Inventaire 
          isOpen={showInventory}
          onClose={() => setShowInventory(false)}
        />
      )}

      {/* Modal de création d'équipe */}
      {showCreateTeamModal && (
        <div className="modal-overlay" onClick={() => setShowCreateTeamModal(false)}>
          <div className="create-team-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>➕ Créer une Équipe</h3>
              <button 
                className="modal-close"
                onClick={() => setShowCreateTeamModal(false)}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-content">
              <form onSubmit={(e) => { e.preventDefault(); createTeam(); }}>
                <div className="form-group">
                  <label>Nom de l'équipe *</label>
                  <input
                    type="text"
                    value={teamForm.name}
                    onChange={(e) => setTeamForm({...teamForm, name: e.target.value})}
                    placeholder="Nom de votre équipe"
                    required
                    maxLength={50}
                  />
                </div>
                
                <div className="form-group">
                  <label>Jeu principal *</label>
                  <select
                    value={teamForm.game}
                    onChange={(e) => setTeamForm({...teamForm, game: e.target.value})}
                    required
                  >
                    <option value="cs2">Counter-Strike 2</option>
                    <option value="lol">League of Legends</option>
                    <option value="wow">World of Warcraft</option>
                    <option value="sc2">StarCraft II</option>
                    <option value="minecraft">Minecraft</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    value={teamForm.description}
                    onChange={(e) => setTeamForm({...teamForm, description: e.target.value})}
                    placeholder="Décrivez votre équipe, votre style de jeu, vos objectifs..."
                    rows={4}
                    maxLength={500}
                  />
                </div>
                
                <div className="form-group">
                  <label>Nombre maximum de membres</label>
                  <select
                    value={teamForm.max_members}
                    onChange={(e) => setTeamForm({...teamForm, max_members: parseInt(e.target.value)})}
                  >
                    <option value={2}>2 membres</option>
                    <option value={3}>3 membres</option>
                    <option value={4}>4 membres</option>
                    <option value={5}>5 membres</option>
                    <option value={6}>6 membres</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={teamForm.is_open}
                      onChange={(e) => setTeamForm({...teamForm, is_open: e.target.checked})}
                    />
                    <span className="checkmark"></span>
                    Équipe ouverte aux candidatures
                  </label>
                  <small>Si décoché, l'équipe sera privée et seuls les membres invités pourront rejoindre</small>
                </div>
                
                <div className="modal-actions">
                  <button 
                    type="button"
                    className="btn-cancel"
                    onClick={() => setShowCreateTeamModal(false)}
                    disabled={teamLoading}
                  >
                    Annuler
                  </button>
                  <button 
                    type="submit"
                    className="btn-confirm"
                    disabled={teamLoading || !teamForm.name}
                  >
                    {teamLoading ? '⏳ Création...' : '➕ Créer l\'équipe'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Modal de gestion d'équipes */}
      {showManageTeamModal && (
        <div className="modal-overlay" onClick={() => setShowManageTeamModal(false)}>
          <div className="manage-team-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>⚙️ Gérer mes Équipes</h3>
              <button 
                className="modal-close"
                onClick={() => setShowManageTeamModal(false)}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-content">
              <div className="teams-management-list">
                {userTeams.length === 0 ? (
                  <div className="no-teams">
                    <div className="no-teams-icon">🤝</div>
                    <p>Vous n'avez pas encore d'équipe</p>
                    <button 
                      className="btn-create-team-inline"
                      onClick={() => {
                        setShowManageTeamModal(false);
                        setShowCreateTeamModal(true);
                      }}
                    >
                      ➕ Créer ma première équipe
                    </button>
                  </div>
                ) : (
                  userTeams.map(team => (
                    <div key={team.id} className="team-management-card">
                      <div className="team-management-header">
                        <div className="team-management-info">
                          <h4>{team.name}</h4>
                          <div className="team-meta">
                            <span className="team-game">{getGameDisplay(team.game)}</span>
                            <span className="team-members">{team.members?.length || 1}/{team.max_members} membres</span>
                            <span className={`team-status ${team.is_open ? 'open' : 'closed'}`}>
                              {team.is_open ? '🟢 Ouverte' : '🔒 Fermée'}
                            </span>
                          </div>
                        </div>
                        <div className="team-role">
                          {team.is_captain ? (
                            <span className="captain-badge">👑 Capitaine</span>
                          ) : (
                            <span className="member-badge">👤 Membre</span>
                          )}
                        </div>
                      </div>
                      
                      <div className="team-management-stats">
                        <div className="stat-item">
                          <span className="stat-label">Tournois</span>
                          <span className="stat-value">{team.statistics?.total_tournaments || 0}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Victoires</span>
                          <span className="stat-value">{team.statistics?.tournaments_won || 0}</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Winrate</span>
                          <span className="stat-value">{team.statistics?.win_rate || 0}%</span>
                        </div>
                      </div>
                      
                      <div className="team-management-actions">
                        {team.is_captain ? (
                          <>
                            <button className="btn-edit-team">📝 Modifier</button>
                            <button className="btn-manage-members">👥 Membres</button>
                            <button 
                              className="btn-delete-team"
                              onClick={() => deleteTeam(team.id)}
                            >
                              🗑️ Supprimer
                            </button>
                          </>
                        ) : (
                          <button 
                            className="btn-leave-team"
                            onClick={() => leaveTeam(team.id)}
                          >
                            🚪 Quitter l'équipe
                          </button>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Communaute;