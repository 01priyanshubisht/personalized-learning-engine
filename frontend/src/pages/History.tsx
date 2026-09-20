import { useEffect, useState, useMemo } from 'react';
import { historyApi } from '../api/history';
import { HistoryEntry } from '../types/api';
import { LEARNER_ID } from '../App';
import { Loader2, BookOpen, GraduationCap, Calendar, Flame, FileText, Target } from 'lucide-react';

const History = () => {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await historyApi.getHistory(LEARNER_ID);
        setHistory(response.history);
      } catch (err: any) {
        console.error(err);
        setError('Failed to load history.');
      } finally {
        setIsLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const stats = useMemo(() => {
    let topics = 0;
    let docs = 0;
    const dates = new Set<string>();

    history.forEach(entry => {
      if (entry.activity_type === 'TOPIC_STUDIED') topics++;
      if (entry.activity_type === 'DOCUMENT_STUDIED') docs++;
      const d = new Date(entry.created_at);
      dates.add(`${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`);
    });

    // Calculate streak
    let currentStreak = 0;
    if (dates.size > 0) {
      const today = new Date();
      const todayStr = `${today.getFullYear()}-${today.getMonth()}-${today.getDate()}`;
      let currDate = new Date(today);
      if (!dates.has(todayStr)) {
        currDate.setDate(currDate.getDate() - 1);
      }
      while (true) {
        const dateStr = `${currDate.getFullYear()}-${currDate.getMonth()}-${currDate.getDate()}`;
        if (dates.has(dateStr)) {
          currentStreak++;
          currDate.setDate(currDate.getDate() - 1);
        } else {
          break;
        }
      }
    }

    return { topics, docs, days: dates.size, streak: currentStreak };
  }, [history]);

  if (isLoading) {
    return (
      <div className="py-32 flex justify-center">
        <Loader2 className="h-10 w-10 text-indigo-600 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-20 text-center text-red-600">
        <p>{error}</p>
      </div>
    );
  }

  // Group by date
  const groupedHistory = history.reduce((acc, entry) => {
    const date = new Date(entry.created_at);
    const dateString = date.toLocaleDateString(undefined, { 
      year: 'numeric', month: 'long', day: 'numeric' 
    });
    
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    let label = dateString;
    if (date.toDateString() === today.toDateString()) {
      label = 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      label = 'Yesterday';
    }

    if (!acc[label]) acc[label] = [];
    acc[label].push(entry);
    return acc;
  }, {} as Record<string, HistoryEntry[]>);

  return (
    <div className="max-w-4xl mx-auto py-4 md:py-8 pb-24 md:pb-8">
      <header className="mb-10">
        <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 tracking-tight">Your Learning History</h1>
        <p className="text-lg text-gray-600 mt-2 font-light">See what you've studied and how your knowledge is growing.</p>
      </header>

      {history.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex flex-col items-center text-center">
            <Flame className="h-6 w-6 text-orange-500 mb-2" />
            <span className="text-2xl font-bold text-gray-900">{stats.streak}</span>
            <span className="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Day Streak</span>
          </div>
          <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex flex-col items-center text-center">
            <Calendar className="h-6 w-6 text-blue-500 mb-2" />
            <span className="text-2xl font-bold text-gray-900">{stats.days}</span>
            <span className="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Study Days</span>
          </div>
          <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex flex-col items-center text-center">
            <Target className="h-6 w-6 text-indigo-500 mb-2" />
            <span className="text-2xl font-bold text-gray-900">{stats.topics}</span>
            <span className="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Topics</span>
          </div>
          <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex flex-col items-center text-center">
            <FileText className="h-6 w-6 text-emerald-500 mb-2" />
            <span className="text-2xl font-bold text-gray-900">{stats.docs}</span>
            <span className="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Documents</span>
          </div>
        </div>
      )}

      {Object.keys(groupedHistory).length === 0 ? (
        <div className="text-center py-20 bg-white rounded-3xl border border-gray-100 shadow-sm">
          <Calendar className="h-16 w-16 text-gray-200 mx-auto mb-6" />
          <h3 className="text-xl font-bold text-gray-900 mb-2">Your learning journey starts here.</h3>
          <p className="text-gray-500 max-w-md mx-auto">Study a topic or upload your notes to begin building your history.</p>
        </div>
      ) : (
        <div className="space-y-10 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-200 before:to-transparent">
          {Object.entries(groupedHistory).map(([dateLabel, entries]) => (
            <div key={dateLabel} className="relative">
              <div className="flex items-center justify-start md:justify-center mb-6">
                <span className="bg-gray-100 text-gray-600 text-sm font-bold px-4 py-1 rounded-full z-10 shadow-sm border border-gray-200 ml-1 md:ml-0">
                  {dateLabel}
                </span>
              </div>
              <div className="space-y-4">
                {entries.map((entry) => (
                  <div key={entry.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
                    {/* Icon */}
                    <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-indigo-100 text-indigo-600 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 ml-0 md:ml-auto md:mr-auto absolute md:static left-0 md:left-auto">
                      {entry.activity_type === 'TOPIC_STUDIED' ? (
                        <GraduationCap className="h-4 w-4" />
                      ) : (
                        <BookOpen className="h-4 w-4" />
                      )}
                    </div>
                    {/* Card */}
                    <div className="w-[calc(100%-3rem)] md:w-[calc(50%-2.5rem)] ml-auto md:ml-0 p-5 rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                      <div className="flex justify-between items-start gap-2 mb-2">
                        <h3 className="font-bold text-gray-900 text-lg leading-tight break-words">
                          {entry.activity_type === 'TOPIC_STUDIED' ? entry.topic : 'Study Material Upload'}
                        </h3>
                        <span className="text-xs font-medium text-gray-400 bg-gray-50 px-2 py-1 rounded-md shrink-0">
                          {new Date(entry.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500 mb-3">
                        {entry.activity_type === 'TOPIC_STUDIED' ? 'Learned a new topic' : (
                          <span>
                            Added to knowledge base
                            {entry.document_id && (
                              <span className="ml-2 font-mono text-xs bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded border border-indigo-100/60 inline-block max-w-[180px] truncate align-middle">
                                ID: {entry.document_id}
                              </span>
                            )}
                          </span>
                        )}
                      </p>
                      
                      {entry.concepts && entry.concepts.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 mt-3 pt-3 border-t border-gray-100">
                          {entry.concepts.map((concept, idx) => (
                            <span key={idx} className="px-2.5 py-1 bg-indigo-50/80 hover:bg-indigo-100 text-indigo-700 text-xs rounded-lg font-medium border border-indigo-100/60 transition-colors">
                              {concept}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;
