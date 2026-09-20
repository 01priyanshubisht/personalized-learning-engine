import { Link, useLocation } from 'react-router-dom';
import { BookOpen } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path ? 'text-indigo-600 font-medium' : 'text-gray-600 hover:text-indigo-600';
  };

  return (
    <nav className="bg-white shadow-sm border-b border-gray-100">
      <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2">
          <BookOpen className="h-6 w-6 text-indigo-600" />
          <span className="text-xl font-bold text-gray-900 tracking-tight">Personalized Learning</span>
        </Link>
        <div className="flex space-x-6">
          <Link to="/" className={isActive('/')}>Dashboard</Link>
          <Link to="/learn" className={isActive('/learn')}>Learn</Link>
          <Link to="/history" className={isActive('/history')}>History</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
