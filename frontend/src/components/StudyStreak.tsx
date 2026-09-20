import { useMemo } from 'react';
import { HistoryEntry } from '../types/api';
import { Flame, Calendar as CalendarIcon, CheckCircle2 } from 'lucide-react';

interface StudyStreakProps {
  history: HistoryEntry[];
}

export const StudyStreak = ({ history }: StudyStreakProps) => {
  const { streak, totalDays, studiedToday } = useMemo(() => {
    const dates = new Set(
      history.map(entry => {
        const d = new Date(entry.created_at);
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      })
    );

    const today = new Date();
    const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    
    const studiedToday = dates.has(todayStr);
    let streak = 0;
    let currDate = new Date(today);

    if (!studiedToday) {
      currDate.setDate(currDate.getDate() - 1);
    }

    while (true) {
      const dateStr = `${currDate.getFullYear()}-${String(currDate.getMonth() + 1).padStart(2, '0')}-${String(currDate.getDate()).padStart(2, '0')}`;
      if (dates.has(dateStr)) {
        streak++;
        currDate.setDate(currDate.getDate() - 1);
      } else {
        break;
      }
    }

    return { streak, totalDays: dates.size, studiedToday };
  }, [history]);

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col items-center justify-center space-y-4">
      <div className="flex items-center space-x-3">
        <div className={`p-3 rounded-full ${studiedToday ? 'bg-orange-100 text-orange-600' : 'bg-gray-100 text-gray-400'}`}>
          <Flame className="h-8 w-8" />
        </div>
        <div>
          <h3 className="text-2xl font-bold text-gray-900">{streak} day streak</h3>
          <p className="text-sm text-gray-500">
            {studiedToday ? "Keep going — you're building a learning habit." : "Start your streak today."}
          </p>
        </div>
      </div>
      
      <div className="flex w-full pt-4 border-t border-gray-50 justify-around text-sm">
        <div className="flex flex-col items-center">
          <span className="text-gray-400 mb-1"><CalendarIcon className="h-4 w-4" /></span>
          <span className="font-semibold text-gray-700">{totalDays} study days</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-gray-400 mb-1"><CheckCircle2 className="h-4 w-4" /></span>
          <span className={`font-semibold ${studiedToday ? 'text-green-600' : 'text-gray-400'}`}>
            {studiedToday ? 'Today ✓' : 'Today ×'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default StudyStreak;
