import { useMemo } from 'react';
import { HistoryEntry } from '../types/api';

interface StudyCalendarProps {
  history: HistoryEntry[];
}

export const StudyCalendar = ({ history }: StudyCalendarProps) => {
  const { weeks } = useMemo(() => {
    const dates = new Set(
      history.map(entry => {
        const d = new Date(entry.created_at);
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      })
    );

    const today = new Date();
    // show last 35 days (5 weeks)
    const weeksArr = [];
    let currentDate = new Date(today);
    // start on the correct day 34 days ago
    currentDate.setDate(currentDate.getDate() - 34);

    for (let w = 0; w < 5; w++) {
      const week = [];
      for (let d = 0; d < 7; d++) {
        const dateStr = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(currentDate.getDate()).padStart(2, '0')}`;
        const isToday = dateStr === `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
        week.push({
          date: new Date(currentDate),
          studied: dates.has(dateStr),
          isToday
        });
        currentDate.setDate(currentDate.getDate() + 1);
      }
      weeksArr.push(week);
    }
    return { weeks: weeksArr, daysTotal: dates.size };
  }, [history]);

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <h3 className="text-lg font-bold text-gray-900 mb-4">Study Activity</h3>
      <div className="flex space-x-2">
        {weeks.map((week, wi) => (
          <div key={wi} className="flex flex-col space-y-2">
            {week.map((day, di) => (
              <div
                key={di}
                title={day.date.toDateString()}
                className={`w-4 h-4 rounded-sm ${day.studied ? 'bg-indigo-500' : 'bg-gray-100'} ${day.isToday && !day.studied ? 'border border-indigo-300' : ''}`}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="flex items-center mt-4 text-xs text-gray-500 space-x-2">
        <span>Less</span>
        <div className="w-3 h-3 rounded-sm bg-gray-100"></div>
        <div className="w-3 h-3 rounded-sm bg-indigo-500"></div>
        <span>More</span>
      </div>
    </div>
  );
};

export default StudyCalendar;
