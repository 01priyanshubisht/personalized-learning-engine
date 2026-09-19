import { Link, useLocation } from 'react-router-dom';
import { BookOpen, LayoutDashboard, History as HistoryIcon, Target } from 'lucide-react';

const Sidebar = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path
      ? 'bg-indigo-50 text-indigo-700 font-semibold'
      : 'text-gray-600 hover:bg-gray-50 hover:text-indigo-600 font-medium';
  };

  return (
    <>
      {/* Mobile Top Navbar */}
      <div className="md:hidden bg-white shadow-sm border-b border-gray-100 px-4 h-16 flex items-center justify-between sticky top-0 z-50">
        <Link to="/" className="flex items-center space-x-2">
          <BookOpen className="h-6 w-6 text-indigo-600" />
          <span className="text-xl font-bold text-gray-900 tracking-tight">LearnEngine</span>
        </Link>
      </div>

      {/* Mobile Bottom Navigation */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 flex justify-around p-3 z-50">
        <Link to="/" className={`flex flex-col items-center ${location.pathname === '/' ? 'text-indigo-600' : 'text-gray-500'}`}>
          <LayoutDashboard className="h-6 w-6 mb-1" />
          <span className="text-xs font-medium">Dashboard</span>
        </Link>
        <Link to="/learn" className={`flex flex-col items-center ${location.pathname === '/learn' ? 'text-indigo-600' : 'text-gray-500'}`}>
          <Target className="h-6 w-6 mb-1" />
          <span className="text-xs font-medium">Learn</span>
        </Link>
        <Link to="/history" className={`flex flex-col items-center ${location.pathname === '/history' ? 'text-indigo-600' : 'text-gray-500'}`}>
          <HistoryIcon className="h-6 w-6 mb-1" />
          <span className="text-xs font-medium">History</span>
        </Link>
      </div>

      {/* Desktop Sidebar */}
      <div className="hidden md:flex flex-col w-64 bg-white border-r border-gray-100 h-screen fixed left-0 top-0 overflow-y-auto">
        <div className="p-6">
          <Link to="/" className="flex items-center space-x-2">
            <BookOpen className="h-7 w-7 text-indigo-600" />
            <span className="text-xl font-extrabold text-gray-900 tracking-tight">LearnEngine</span>
          </Link>
        </div>

        <nav className="flex-1 px-4 space-y-2 mt-4">
          <Link to="/" className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-colors ${isActive('/')}`}>
            <LayoutDashboard className="h-5 w-5" />
            <span>Dashboard</span>
          </Link>
          <Link to="/learn" className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-colors ${isActive('/learn')}`}>
            <Target className="h-5 w-5" />
            <span>Learn</span>
          </Link>
          <Link to="/history" className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-colors ${isActive('/history')}`}>
            <HistoryIcon className="h-5 w-5" />
            <span>History</span>
          </Link>
        </nav>

        <div className="p-6 mt-auto">
          <div className="bg-gradient-to-r from-indigo-500 to-blue-600 rounded-2xl p-4 text-white shadow-md">
            <h4 className="font-bold mb-1">Keep growing</h4>
            <p className="text-xs text-indigo-100 mb-3">Upload notes to build your knowledge base.</p>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
