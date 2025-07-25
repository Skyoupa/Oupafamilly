import React from 'react';
import { Link } from 'react-router-dom';

const APropos = () => {
  const timeline = [
    {
      year: '2023',
      title: 'Les Origines',
      description: 'Création de la Oupafamilly par un groupe d\'amis passionnés de gaming et d\'esports compétitif.',
      milestone: 'Fondation'
    },
    {
      year: '2023',
      title: 'Premiers Tournois',
      description: 'Organisation des premiers tournois internes sur Counter-Strike 2 et League of Legends avec succès.',
      milestone: 'Compétition'
    },
    {
      year: '2024',
      title: 'Expansion Multi-Gaming',
      description: 'Ajout de World of Warcraft, StarCraft II et Minecraft. Croissance jusqu\'à 100 membres actifs.',
      milestone: 'Croissance'
    },
    {
      year: '2024',
      title: 'Reconnaissance Esports',
      description: 'Victoires dans plusieurs tournois régionaux et création d\'équipes compétitives professionnelles.',
      milestone: 'Excellence'
    },
    {
      year: '2025',
      title: 'Communauté d\'Élite',
      description: 'Plus de 150 membres actifs, 50+ tournois organisés et reconnaissance comme communauté de référence.',
      milestone: 'Légendaire'
    }
  ];

  const values = [
    {
      icon: (
        <svg className="value-icon-svg-detailed" viewBox="0 0 64 64" fill="none">
          <circle cx="32" cy="32" r="28" stroke="currentColor" strokeWidth="3" fill="rgba(59, 130, 246, 0.1)"/>
          <path d="M20 32L28 40L44 24" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      title: 'Excellence Compétitive',
      description: 'Nous visons l\'excellence dans chaque match et tournoi. Notre approche professionnelle du gaming nous distingue.',
      details: [
        'Coaching personnalisé pour chaque membre',
        'Analyses détaillées des performances',
        'Stratégies éprouvées et méta actualisée',
        'Mentalité de champion dans chaque match'
      ]
    },
    {
      icon: (
        <svg className="value-icon-svg-detailed" viewBox="0 0 64 64" fill="none">
          <rect x="12" y="20" width="40" height="28" rx="4" stroke="currentColor" strokeWidth="3" fill="rgba(59, 130, 246, 0.1)"/>
          <path d="M18 32h28M18 38h20" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <circle cx="42" cy="35" r="3" fill="currentColor"/>
        </svg>
      ),
      title: 'Stratégie Professionnelle',
      description: 'Chaque membre bénéficie d\'un accompagnement tactique et d\'analyses approfondies pour progresser.',
      details: [
        'Plans tactiques détaillés par jeu',
        'Sessions de review et débriefing',
        'Veille technologique et méta gaming',
        'Formation continue aux nouvelles techniques'
      ]
    },
    {
      icon: (
        <svg className="value-icon-svg-detailed" viewBox="0 0 64 64" fill="none">
          <circle cx="32" cy="25" r="8" stroke="currentColor" strokeWidth="3" fill="rgba(59, 130, 246, 0.1)"/>
          <path d="M20 45c0-8 5-12 12-12s12 4 12 12" stroke="currentColor" strokeWidth="3"/>
          <path d="M15 52h34" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/>
        </svg>
      ),
      title: 'Esprit Familial',
      description: 'Plus qu\'une team, nous formons une véritable famille unie où chaque membre compte et contribue.',
      details: [
        'Soutien mutuel inconditionnel',
        'Intégration facilitée des nouveaux membres',
        'Événements communautaires réguliers',
        'Liens durables au-delà du gaming'
      ]
    },
    {
      icon: (
        <svg className="value-icon-svg-detailed" viewBox="0 0 64 64" fill="none">
          <path d="M32 8L42 22H22L32 8z" stroke="currentColor" strokeWidth="3" fill="rgba(59, 130, 246, 0.1)"/>
          <rect x="22" y="22" width="20" height="20" stroke="currentColor" strokeWidth="3" fill="rgba(59, 130, 246, 0.1)"/>
          <path d="M27 47h10v8h-10z" stroke="currentColor" strokeWidth="3" fill="currentColor"/>
        </svg>
      ),
      title: 'Innovation Gaming',
      description: 'Toujours à la pointe des méta et techniques, nous adaptons constamment nos stratégies et méthodes.',
      details: [
        'Recherche et développement gaming',
        'Adaptation rapide aux évolutions',
        'Outils et technologies de pointe',
        'Expérimentation de nouvelles approches'
      ]
    }
  ];

  const team = [
    {
      name: 'Alexandre',
      role: 'Fondateur & CEO',
      pseudo: 'AlexTheKing',
      description: 'Visionnaire et stratège, Alex a créé la Oupafamilly avec l\'ambition de rassembler l\'élite du gaming francophone.',
      specialties: ['Leadership', 'Stratégie globale', 'CS2 Pro', 'Management'],
      achievements: ['Fondateur communauté', 'Ex-pro CS', 'Coach certifié']
    },
    {
      name: 'Marie',
      role: 'Community Manager',
      pseudo: 'MariGamer',
      description: 'Responsable de l\'animation et de la cohésion de notre communauté, Marie veille au bien-être de chaque membre.',
      specialties: ['Animation', 'Communication', 'WoW Expert', 'Event Management'],
      achievements: ['Top 1% WoW', 'Event Manager', 'Community Expert']
    },
    {
      name: 'Thomas',
      role: 'Head Coach',
      pseudo: 'TomStrat',
      description: 'Ancien joueur professionnel, Tom dirige nos programmes de coaching et développe nos stratégies compétitives.',
      specialties: ['Coaching', 'Analyse tactique', 'SC2 Master', 'Formation'],
      achievements: ['Ex-pro SC2', 'Master Coach', 'Analyste expert']
    }
  ];

  const stats = [
    { number: '150+', label: 'Membres d\'élite', description: 'Une communauté sélective' },
    { number: '5', label: 'Jeux maîtrisés', description: 'Expertise multi-gaming' },
    { number: '50+', label: 'Tournois organisés', description: 'Organisation professionnelle' },
    { number: '2', label: 'Années d\'excellence', description: 'Expérience et stabilité' }
  ];

  return (
    <div className="page-pro">
      {/* Header */}
      <section className="page-header-pro about-header">
        <div className="about-bg">
          <div className="about-overlay"></div>
          <div className="about-pattern"></div>
        </div>
        <div className="container-pro">
          <div className="about-badge">
            <svg className="about-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z"/>
            </svg>
            <span>NOTRE HISTOIRE</span>
          </div>
          <h1 className="page-title-pro about-title">À PROPOS</h1>
          <p className="page-subtitle-pro">
            L'histoire, les valeurs et l'équipe derrière la communauté gaming d'élite
          </p>
        </div>
      </section>

      {/* Stats */}
      <section className="section-pro">
        <div className="container-pro">
          <div className="about-stats-pro">
            {stats.map((stat, index) => (
              <div key={index} className="about-stat-card">
                <div className="stat-number-large">{stat.number}</div>
                <div className="stat-label-large">{stat.label}</div>
                <div className="stat-description">{stat.description}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Story */}
      <section className="section-pro section-alt-pro">
        <div className="container-pro">
          <div className="story-section-pro">
            <div className="story-content-pro">
              <div className="section-header-pro">
                <div className="section-badge">
                  <span>NOTRE PARCOURS</span>
                </div>
                <h2 className="section-title-pro">L'Histoire Oupafamilly</h2>
              </div>
              <div className="story-text-pro">
                <p>
                  La Oupafamilly est née en 2023 de la passion commune d'un groupe d'amis pour le gaming compétitif. 
                  Frustrés par la toxicité présente dans de nombreuses communautés, nous avons décidé de créer un espace 
                  où l'excellence rencontre la bienveillance.
                </p>
                <p>
                  Ce qui a commencé comme un petit groupe de joueurs passionnés s'est rapidement transformé en une 
                  communauté d'élite reconnue. Aujourd'hui, nous sommes fiers de compter plus de 150 membres actifs 
                  partageant nos valeurs d'excellence et d'esprit familial.
                </p>
                <p>
                  Notre mission demeure simple mais ambitieuse : offrir à chaque membre un environnement d'exception 
                  où il peut s'épanouir, progresser et créer des liens durables avec d'autres passionnés de gaming.
                </p>
              </div>
            </div>
            <div className="story-visual-pro">
              <div className="story-logo-pro">
                <img 
                  src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath d='M50 10 L85 25 L85 65 Q85 80 50 90 Q15 80 15 65 L15 25 Z' fill='%233b82f6'/%3E%3Ctext x='50' y='55' text-anchor='middle' fill='%23ffffff' font-family='Arial Black' font-size='14' font-weight='bold'%3EOUPA%3C/text%3E%3C/svg%3E" 
                  alt="Oupafamilly Logo" 
                  className="story-logo-img"
                />
                <div className="story-logo-text">OUPAFAMILLY</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="section-pro">
        <div className="container-pro">
          <div className="section-header-pro">
            <div className="section-badge">
              <span>CHRONOLOGIE</span>
            </div>
            <h2 className="section-title-pro">Notre Évolution</h2>
            <p className="section-subtitle-pro">Les étapes clés de notre développement</p>
          </div>
          <div className="timeline-pro">
            {timeline.map((event, index) => (
              <div key={index} className="timeline-item-pro">
                <div className="timeline-marker-pro">
                  <span className="timeline-year">{event.year}</span>
                </div>
                <div className="timeline-content-pro">
                  <div className="timeline-milestone">{event.milestone}</div>
                  <h3 className="timeline-title">{event.title}</h3>
                  <p className="timeline-description">{event.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Values Detail */}
      <section className="section-pro section-alt-pro">
        <div className="container-pro">
          <div className="section-header-pro">
            <div className="section-badge">
              <span>NOS PRINCIPES</span>
            </div>
            <h2 className="section-title-pro">Nos Valeurs en Détail</h2>
            <p className="section-subtitle-pro">Les piliers qui définissent notre identité</p>
          </div>
          <div className="values-detail-pro">
            {values.map((value, index) => (
              <div key={index} className="value-detail-card-pro">
                <div className="value-detail-header-pro">
                  <div className="value-detail-icon-pro">{value.icon}</div>
                  <h3 className="value-detail-title-pro">{value.title}</h3>
                </div>
                <p className="value-detail-description-pro">{value.description}</p>
                <ul className="value-detail-list-pro">
                  {value.details.map((detail, detailIndex) => (
                    <li key={detailIndex} className="value-detail-item-pro">
                      <svg className="checkmark-icon" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      {detail}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="section-pro">
        <div className="container-pro">
          <div className="section-header-pro">
            <div className="section-badge">
              <span>LEADERSHIP</span>
            </div>
            <h2 className="section-title-pro">L'Équipe Dirigeante</h2>
            <p className="section-subtitle-pro">Les visionnaires qui guident la communauté</p>
          </div>
          <div className="team-grid-pro">
            {team.map((member, index) => (
              <div key={index} className="team-member-card-pro">
                <div className="team-member-avatar-pro">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 12C14.21 12 16 10.21 16 8S14.21 4 12 4 8 5.79 8 8 9.79 12 12 12M12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z"/>
                  </svg>
                </div>
                <div className="team-member-info-pro">
                  <h3 className="team-member-name-pro">{member.name}</h3>
                  <p className="team-member-role-pro">{member.role}</p>
                  <p className="team-member-pseudo-pro">@{member.pseudo}</p>
                </div>
                <p className="team-member-description-pro">{member.description}</p>
                <div className="team-member-specialties-pro">
                  <h4>Spécialités</h4>
                  <div className="specialties-list">
                    {member.specialties.map((specialty, specIndex) => (
                      <span key={specIndex} className="specialty-tag-pro">
                        {specialty}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="team-member-achievements-pro">
                  <h4>Réalisations</h4>
                  <ul>
                    {member.achievements.map((achievement, achIndex) => (
                      <li key={achIndex}>
                        <svg className="achievement-icon" viewBox="0 0 20 20" fill="currentColor">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                        {achievement}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="cta-section-pro">
        <div className="cta-bg">
          <div className="cta-pattern"></div>
        </div>
        <div className="container-pro">
          <div className="cta-content-pro">
            <div className="cta-badge">
              <span>REJOIGNEZ L'AVENTURE</span>
            </div>
            <h2 className="cta-title-pro">Prêt à faire partie de l'histoire ?</h2>
            <p className="cta-subtitle-pro">
              Découvrez une communauté d'exception où passion et excellence se rencontrent
            </p>
            <div className="cta-buttons-pro">
              <Link to="/communaute" className="btn-primary-pro btn-large">
                <span>REJOINDRE LA COMMUNAUTÉ</span>
                <svg className="btn-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </Link>
              <Link to="/tournois" className="btn-outline-pro">
                <span>VOIR LES TOURNOIS</span>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default APropos;