import { Link } from 'react-router-dom';
import { Dna, ScanSearch, Lightbulb, MessageSquareText } from 'lucide-react';
import { useUserStore } from '../../store/userStore';
import { useProjectStore } from '../../store/projectStore';
import { useAnalysisList } from '../../features/sculpture/hooks/useSculptureAnalysis';
import { useIdeaList } from '../../features/ideas/hooks/useIdeas';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Skeleton } from '../../components/ui/Skeleton';

export default function Dashboard() {
  const { user } = useUserStore();
  const { currentProject } = useProjectStore();
  const { data: analyses, isLoading: isLoadingAnalyses } = useAnalysisList();
  const { data: ideas, isLoading: isLoadingIdeas } = useIdeaList();

  const quickActions = [
    { title: 'Style DNA', desc: 'Extract aesthetic traits', icon: Dna, path: '/style-dna', color: 'text-primary-500' },
    { title: 'Sculpture Analyzer', desc: 'Analyze forms & materials', icon: ScanSearch, path: '/sculpture', color: 'text-secondary-500' },
    { title: 'Idea Generator', desc: 'AI concept generation', icon: Lightbulb, path: '/ideas', color: 'text-accent-500' },
    { title: 'Critique Mode', desc: 'Multi-persona review', icon: MessageSquareText, path: '/critique', color: 'text-emerald-500' },
  ];

  return (
    <div className="space-y-8 animate-fade-in">
      <header>
        <h1 className="text-3xl font-bold text-surface-900 dark:text-white mb-2">
          Welcome back, <span className="gradient-text">{user?.name?.split(' ')[0]}</span>
        </h1>
        <p className="text-surface-500 dark:text-surface-400">
          Here's an overview of your creative projects today.
        </p>
      </header>

      {currentProject && (
        <Card className="p-6 border-l-4 border-l-primary-500 bg-gradient-to-r from-surface-50 to-white dark:from-surface-900 dark:to-surface-800">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <p className="text-xs font-semibold text-primary-600 dark:text-primary-400 uppercase tracking-wider mb-1">
                Active Project
              </p>
              <h2 className="text-xl font-bold text-surface-900 dark:text-white mb-2">
                {currentProject.name}
              </h2>
              <p className="text-sm text-surface-600 dark:text-surface-300 max-w-2xl">
                {currentProject.description}
              </p>
            </div>
            <div className="flex gap-4 sm:justify-end">
              <div className="text-center">
                <div className="text-2xl font-black text-surface-900 dark:text-white">{currentProject.imageCount}</div>
                <div className="text-xs font-medium text-surface-500 uppercase">Assets</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-black text-surface-900 dark:text-white">{currentProject.analysisCount}</div>
                <div className="text-xs font-medium text-surface-500 uppercase">Analyses</div>
              </div>
            </div>
          </div>
        </Card>
      )}

      <div>
        <h3 className="text-lg font-bold text-surface-900 dark:text-white mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map(action => (
            <Link key={action.path} to={action.path} className="block group">
              <Card hover className="p-4 h-full transition-colors group-hover:border-primary-500">
                <action.icon className={`w-8 h-8 mb-3 ${action.color}`} />
                <h4 className="font-semibold text-surface-900 dark:text-white mb-1 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                  {action.title}
                </h4>
                <p className="text-xs text-surface-500 line-clamp-2">{action.desc}</p>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-surface-900 dark:text-white">Recent Analyses</h3>
            <Link to="/sculpture" className="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
              View all
            </Link>
          </div>
          <div className="space-y-3">
            {isLoadingAnalyses ? (
              Array(3).fill(0).map((_, i) => <Skeleton key={i} className="h-20 w-full rounded-xl" />)
            ) : analyses?.slice(0, 3).map(analysis => (
              <Card key={analysis.id} className="p-4 flex items-center justify-between hover:bg-surface-50 dark:hover:bg-surface-800/50 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-lg bg-surface-200 dark:bg-surface-700 overflow-hidden shrink-0">
                    <img src={analysis.imageUrl} alt="Analysis" className="w-full h-full object-cover" />
                  </div>
                  <div>
                    <h4 className="font-medium text-surface-900 dark:text-white truncate max-w-[200px]">{analysis.fileName}</h4>
                    <p className="text-xs text-surface-500">
                      {new Date(analysis.createdAt).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <Badge variant="primary" size="sm">{analysis.period}</Badge>
              </Card>
            ))}
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-surface-900 dark:text-white">Recent Concepts</h3>
            <Link to="/ideas" className="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
              View all
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {isLoadingIdeas ? (
              Array(4).fill(0).map((_, i) => <Skeleton key={i} className="h-32 w-full rounded-xl" />)
            ) : ideas?.slice(0, 4).map(idea => (
              <Card key={idea.id} className="p-4 hover:bg-surface-50 dark:hover:bg-surface-800/50 transition-colors flex flex-col">
                <h4 className="font-medium text-surface-900 dark:text-white line-clamp-1 mb-1">{idea.title}</h4>
                <p className="text-xs text-surface-500 line-clamp-2 mb-3 flex-1">{idea.concept}</p>
                <div className="flex justify-between items-center mt-auto">
                  <Badge variant="secondary" size="sm" className="capitalize">{idea.status}</Badge>
                  <Link to="/ideas" className="text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline">
                    Read more
                  </Link>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
