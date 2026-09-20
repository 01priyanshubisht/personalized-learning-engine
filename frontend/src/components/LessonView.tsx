import { LearningResponse } from '../types/api';
import {
  CheckCircle2,
  Circle,
  Target,
  FileText,
  Lightbulb,
  BookOpen
} from 'lucide-react';

interface LessonViewProps {
  lessonData: LearningResponse;
  topic: string;
}

const renderFormattedText = (text: string) => {
  if (!text) return null;
  const parts = text.split(/(\*\*.*?\*\*)/g);
  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**') && part.length > 4) {
      return (
        <strong key={index} className="font-semibold text-gray-900">
          {part.slice(2, -2)}
        </strong>
      );
    }
    return part;
  });
};

const LessonView = ({ lessonData, topic }: LessonViewProps) => {
  const { gaps, retrieved_material, lesson } = lessonData;

  const knownConcepts = (gaps || []).filter((gap) => gap.known).map((gap) => gap.concept);
  const unknownConcepts = (gaps || []).filter((gap) => !gap.known).map((gap) => gap.concept);

  return (
    <div className="space-y-12 py-6 pb-24 md:pb-8">
      {/* ================= HEADER ================= */}
      <header className="mb-8">
        <div className="inline-flex items-center space-x-2 bg-indigo-50 text-indigo-700 px-4 py-2 rounded-full font-semibold text-sm mb-4 border border-indigo-100">
          <Target className="w-4 h-4" />
          <span>Personalized Lesson</span>
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight">
          Learning: {lessonData.topic || topic}
        </h1>
      </header>

      {/* ================= MAIN CONTENT ================= */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
        
        {/* ================= LEFT SIDE (30%) ================= */}
        <div className="lg:col-span-4 space-y-8">
          
          {/* ================= LEARNING PATH ================= */}
          <section className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 sticky top-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Learning Path</h2>
            <div className="space-y-4">
              
              {/* KNOWN CONCEPTS */}
              {knownConcepts.map((concept, idx) => (
                <div key={`known-${idx}`} className="flex items-start space-x-3 p-3 rounded-xl bg-green-50 border border-green-100/50 transition-colors">
                  <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-green-900">{concept}</p>
                    <p className="text-xs text-green-700">Known concept</p>
                  </div>
                </div>
              ))}

              {/* UNKNOWN CONCEPTS */}
              {unknownConcepts.map((concept, idx) => (
                <div key={`unknown-${idx}`} className="flex items-start space-x-3 p-3 rounded-xl bg-amber-50 border border-amber-100/50 transition-colors">
                  <Circle className="h-5 w-5 text-amber-500 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-amber-900">{concept}</p>
                    <p className="text-xs text-amber-700">New concept</p>
                  </div>
                </div>
              ))}

              {/* TARGET TOPIC */}
              <div className="flex items-start space-x-3 p-3 rounded-xl bg-indigo-50 border border-indigo-100 shadow-sm mt-6">
                <Target className="h-5 w-5 text-indigo-600 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold text-indigo-900">{lessonData.topic || topic}</p>
                  <p className="text-xs text-indigo-700">Target goal</p>
                </div>
              </div>
            </div>
          </section>

          {/* ================= RETRIEVED MATERIAL ================= */}
          {retrieved_material && retrieved_material.length > 0 && (
            <section className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                <FileText className="h-5 w-5 mr-2 text-indigo-600" />
                From your notes
              </h3>
              <div className="space-y-4">
                {retrieved_material.map((mat, idx) => (
                  <div key={idx} className="bg-gray-50 p-4 rounded-xl border border-gray-100 text-sm hover:shadow-sm transition-shadow">
                    <div className="flex items-center space-x-2 mb-2 text-indigo-700 font-semibold">
                      <BookOpen className="w-4 h-4" />
                      <span>Page {mat.page_number}</span>
                    </div>
                    <p className="text-gray-600 italic line-clamp-4 leading-relaxed">"{mat.text}"</p>
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>

        {/* ================= RIGHT SIDE (70%) ================= */}
        <div className="lg:col-span-8 space-y-8">
          
          <section className="bg-white p-8 md:p-10 rounded-3xl shadow-sm border border-gray-100">
            
            {/* ================= PERSONALIZATION PROOF ================= */}
            {knownConcepts.length > 0 && (
              <div className="mb-10 p-6 bg-gradient-to-br from-indigo-50 to-blue-50 rounded-2xl border border-indigo-100/50 shadow-inner">
                <div className="flex items-center space-x-3 mb-3">
                  <Lightbulb className="h-6 w-6 text-indigo-600" />
                  <h3 className="text-xl font-bold text-indigo-900">You already know</h3>
                </div>
                <p className="text-indigo-800 text-lg leading-relaxed">
                  Because you already know <span className="font-bold">{knownConcepts.join(', ')}</span>, we use them as building blocks instead of teaching them from scratch.
                </p>
              </div>
            )}

            {/* ================= GENERATED LESSON ================= */}
            <article className="prose prose-lg max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 prose-a:text-indigo-600 prose-strong:text-indigo-900">
              {!lesson ? (
                <p className="text-gray-500 italic">No lesson content was generated.</p>
              ) : (
                <div className="space-y-12">
                  
                  {/* LESSON INTRO */}
                  <div className="pb-8 border-b border-gray-100">
                    <h2 className="text-3xl font-bold mb-6">{lesson.topic}</h2>
                    <p className="text-xl leading-relaxed text-gray-600">{renderFormattedText(lesson.introduction)}</p>
                  </div>

                  {/* LESSON SECTIONS */}
                  {lesson.sections && lesson.sections.map((section, idx) => (
                    <div key={idx} className="space-y-4">
                      <h3 className="text-2xl font-bold text-gray-900 flex items-center">
                        <span className="bg-indigo-100 text-indigo-700 w-8 h-8 rounded-lg flex items-center justify-center text-sm mr-3">{idx + 1}</span>
                        {section.title}
                      </h3>
                      <p className="leading-relaxed text-gray-700 whitespace-pre-wrap">{renderFormattedText(section.content)}</p>
                    </div>
                  ))}

                  {/* SUMMARY */}
                  {lesson.summary && (
                    <div className="bg-gray-50 border border-gray-200 rounded-2xl p-8 mt-12">
                      <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                        <CheckCircle2 className="w-6 h-6 mr-2 text-green-500" />
                        Summary
                      </h3>
                      <p className="leading-relaxed text-gray-700 whitespace-pre-wrap">{renderFormattedText(lesson.summary)}</p>
                    </div>
                  )}

                  {/* SOURCES */}
                  {lesson.sources && lesson.sources.length > 0 && (
                    <div className="pt-10 border-t border-gray-100">
                      <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center">
                        <FileText className="w-5 h-5 mr-2 text-gray-500" />
                        Sources Used
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {lesson.sources.map((source, idx) => (
                          <div key={idx} className="flex items-start gap-4 bg-white border border-gray-200 rounded-xl p-4 hover:border-indigo-200 hover:shadow-sm transition-all">
                            <div className="bg-indigo-50 p-2 rounded-lg">
                              <FileText className="h-5 w-5 text-indigo-600" />
                            </div>
                            <div>
                              <p className="text-sm font-semibold text-gray-900 truncate">
                                {source.document_id || 'Study Material'}
                              </p>
                              {source.page_number !== null && (
                                <p className="text-xs text-gray-500 mt-1">Page {source.page_number}</p>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </article>
          </section>
        </div>
      </div>
    </div>
  );
};

export default LessonView;