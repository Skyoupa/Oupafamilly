import React from 'react';

const ResourcesHub = ({ game, tutorialTitle }) => {
  // Ressources spécialisées par jeu avec vrais liens
  const gameResources = {
    cs2: {
      title: "Ressources Counter-Strike 2",
      resources: [
        {
          category: "Statistiques Professionnelles",
          links: [
            { name: "HLTV.org", url: "https://www.hltv.org/", description: "Stats équipes pro et rankings" },
            { name: "Liquipedia CS2", url: "https://liquipedia.net/counterstrike/", description: "Base données complète" },
            { name: "Leetify", url: "https://leetify.com/", description: "Analyse performance automatique" }
          ]
        },
        {
          category: "Entraînement et Practice",
          links: [
            { name: "aim_botz Workshop", url: "steam://url/GameHub/730", description: "Map aim training essentielle" },
            { name: "Recoil Master", url: "steam://url/GameHub/730", description: "Practice spray patterns" },
            { name: "Yprac Maps", url: "steam://url/GameHub/730", description: "Prefire practice complet" }
          ]
        },
        {
          category: "Communauté et Guides",
          links: [
            { name: "r/GlobalOffensive", url: "https://reddit.com/r/GlobalOffensive", description: "Reddit communauté active" },
            { name: "FACEIT", url: "https://www.faceit.com/", description: "Plateforme compétitive" },
            { name: "ESL Play", url: "https://play.eslgaming.com/", description: "Tournois officiels" }
          ]
        }
      ]
    },
    lol: {
      title: "Ressources League of Legends",
      resources: [
        {
          category: "Données Professionnelles",
          links: [
            { name: "Liquipedia LoL", url: "https://liquipedia.net/leagueoflegends/", description: "Infos tournaments complètes" },
            { name: "LoL Esports", url: "https://lolesports.com/", description: "Matchs professionnels officiels" },
            { name: "OP.GG", url: "https://op.gg/", description: "Stats et builds pros temps réel" }
          ]
        },
        {
          category: "Outils d'Analyse",
          links: [
            { name: "ProBuilds", url: "https://probuilds.net/", description: "Builds joueurs pro live" },
            { name: "Mobalytics", url: "https://mobalytics.gg/", description: "Analyse performance détaillée" },
            { name: "Blitz.gg", url: "https://blitz.gg/", description: "Coaching automatique" }
          ]
        },
        {
          category: "Éducation",
          links: [
            { name: "Coach Curtis YouTube", url: "https://youtube.com/@CoachCurtis", description: "Macro concepts approfondis" },
            { name: "LS Coaching", url: "https://youtube.com/@LSXYZ9", description: "Draft et macro theory" },
            { name: "r/summonerschool", url: "https://reddit.com/r/summonerschool", description: "Apprentissage communautaire" }
          ]
        }
      ]
    },
    sc2: {
      title: "Ressources StarCraft II",
      resources: [
        {
          category: "Informations Techniques",
          links: [
            { name: "Liquipedia SC2", url: "https://liquipedia.net/starcraft2/", description: "Base données build orders" },
            { name: "Spawning Tool", url: "https://spawningtool.com/", description: "Build orders professionnels" },
            { name: "SC2ReplayStats", url: "https://sc2replaystats.com/", description: "Analyse replays avancée" }
          ]
        },
        {
          category: "Entraînement",
          links: [
            { name: "Ladder Maps", url: "https://sc2ai.net/", description: "Maps ladder officielles" },
            { name: "Practice Partners", url: "https://discord.gg/starcraft", description: "Partenaires d'entraînement" },
            { name: "Build Order Tester", url: "https://lotv.spawningtool.com/", description: "Test build orders" }
          ]
        }
      ]
    },
    wow: {
      title: "Ressources World of Warcraft",
      resources: [
        {
          category: "Guides et Données",
          links: [
            { name: "Liquipedia WoW", url: "https://liquipedia.net/warcraft/", description: "Tournois et équipes pro" },
            { name: "WoWHead", url: "https://www.wowhead.com/", description: "Base données complète" },
            { name: "Raider.IO", url: "https://raider.io/", description: "Classements Mythic+" }
          ]
        },
        {
          category: "Optimisation",
          links: [
            { name: "SimulationCraft", url: "https://simulationcraft.org/", description: "Simulation DPS avancée" },
            { name: "WarcraftLogs", url: "https://warcraftlogs.com/", description: "Analyse logs raids" },
            { name: "Method Guides", url: "https://method.gg/", description: "Guides niveau mythique" }
          ]
        }
      ]
    },
    minecraft: {
      title: "Ressources Minecraft",
      resources: [
        {
          category: "Techniques et Builds",
          links: [
            { name: "Minecraft Wiki", url: "https://minecraft.wiki/", description: "Documentation officielle" },
            { name: "r/Minecraft", url: "https://reddit.com/r/Minecraft", description: "Communauté créative" },
            { name: "Redstone Community", url: "https://reddit.com/r/redstone", description: "Circuits et automatisation" }
          ]
        },
        {
          category: "Serveurs et Mods",
          links: [
            { name: "CurseForge", url: "https://curseforge.com/minecraft", description: "Mods et modpacks" },
            { name: "Planet Minecraft", url: "https://planetminecraft.com/", description: "Maps et créations" },
            { name: "Hypixel", url: "https://hypixel.net/", description: "Serveur mini-jeux populaire" }
          ]
        }
      ]
    }
  };

  const currentGameResources = gameResources[game] || gameResources.cs2;

  return (
    <div className="bg-gray-800 rounded-lg p-6 mb-6">
      <h3 className="text-xl font-bold text-white mb-4 flex items-center">
        <span className="text-blue-400 mr-2">🔗</span>
        {currentGameResources.title}
      </h3>
      
      <div className="space-y-6">
        {currentGameResources.resources.map((category, categoryIndex) => (
          <div key={categoryIndex}>
            <h4 className="text-lg font-semibold text-gray-300 mb-3 border-b border-gray-600 pb-1">
              {category.category}
            </h4>
            <div className="grid gap-3">
              {category.links.map((link, linkIndex) => (
                <a
                  key={linkIndex}
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-3 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors group"
                >
                  <div className="flex-1">
                    <div className="flex items-center">
                      <span className="font-medium text-white group-hover:text-blue-400 transition-colors">
                        {link.name}
                      </span>
                      <span className="ml-2 text-gray-400 text-sm">↗</span>
                    </div>
                    <p className="text-gray-400 text-sm mt-1">{link.description}</p>
                  </div>
                </a>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResourcesHub;