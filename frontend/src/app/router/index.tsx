import { createBrowserRouter } from 'react-router-dom';
import { AppLayout } from '../../components/layout';
import Dashboard from '../../pages/Dashboard';
import StyleDNA from '../../pages/StyleDNA';
import SculptureAnalyzer from '../../pages/SculptureAnalyzer';
import IdeaGenerator from '../../pages/IdeaGenerator';
import CritiqueMode from '../../pages/CritiqueMode';
import Settings from '../../pages/Settings';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'style-dna', element: <StyleDNA /> },
      { path: 'sculpture', element: <SculptureAnalyzer /> },
      { path: 'ideas', element: <IdeaGenerator /> },
      { path: 'critique', element: <CritiqueMode /> },
      { path: 'settings', element: <Settings /> },
    ],
  },
]);
