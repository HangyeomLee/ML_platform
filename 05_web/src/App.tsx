import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Sparkles, List, Send, CheckCircle2, Loader2, Upload, Globe, Instagram, Twitter, BookOpen, MessageCircle, Heart, User, Image as ImageIcon } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

interface Job {
  job_id: string;
  task: string;
  status: string;
  pipeline_step?: string;
  result?: any;
  error?: string;
}

export default function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [lang, setLang] = useState('ko');
  const [platform, setPlatform] = useState('instagram');
  const [tone, setTone] = useState('friendly');
  
  // Image upload states
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const createJob = async () => {
    if (!selectedFile) {
      alert('상품 사진을 업로드해주세요!');
      return;
    }

    setLoading(true);
    try {
      const payload = { 
        task: 'marketing_pipeline',
        language: lang,
        platform,
        tone,
        input: { 
          image_name: selectedFile?.name,
          image_size: selectedFile?.size 
        }
      };
      
      const res = await axios.post(`${API_BASE}/v1/jobs`, payload);
      const newJob: Job = {
        job_id: res.data.job_id,
        task: payload.task,
        status: 'queued'
      };
      setJobs(prev => [newJob, ...prev]);
    } catch (err) {
      alert('요청에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const pollInterval = setInterval(() => {
      const activeJobs = jobs.filter(j => j.status === 'queued' || j.status === 'running');
      activeJobs.forEach(async (job) => {
        try {
          const res = await axios.get(`${API_BASE}/v1/jobs/${job.job_id}`);
          const data = res.data as any;
          if (data.status !== job.status || data.pipeline_step !== job.pipeline_step) {
            setJobs(prev => prev.map(p => 
              p.job_id === job.job_id ? { ...p, status: data.status, pipeline_step: data.pipeline_step, result: data.result, error: data.error } : p
            ));
          }
        } catch (e) { console.error(e); }
      });
    }, 1500);
    return () => clearInterval(pollInterval);
  }, [jobs]);

  return (
    <div className="container" style={{ maxWidth: '1200px' }}>
      <header className="header" style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 className="title" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem', fontSize: '2.5rem' }}>
          <Sparkles size={40} color="#3b82f6" /> 
          AI Marketing Factory
        </h1>
        <p className="subtitle" style={{ fontSize: '1.1rem' }}>사진 한 장으로 전 세계 채널에 맞는 마케팅 콘텐츠를 자동 생성합니다.</p>
      </header>

      <div className="grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
        {/* Left: Configuration Area */}
        <aside className="card" style={{ padding: '2rem' }}>
          <h2 className="card-title" style={{ borderBottom: '1px solid #334155', paddingBottom: '1rem' }}>
            <ImageIcon size={24} /> Step 1. 상품 사진 업로드
          </h2>
          
          <div className="form-group" style={{ marginTop: '1.5rem' }}>
            <div 
              onClick={() => fileInputRef.current?.click()}
              style={{ 
                border: '2px dashed #3b82f6', 
                borderRadius: '16px', 
                padding: '2rem', 
                textAlign: 'center',
                cursor: 'pointer',
                background: '#0f172a',
                transition: 'all 0.3s ease',
                minHeight: '250px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              {previewUrl ? (
                <img src={previewUrl} alt="Preview" style={{ maxWidth: '100%', maxHeight: '300px', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.5)' }} />
              ) : (
                <div style={{ color: '#64748b' }}>
                  <Upload size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
                  <p style={{ fontSize: '1.1rem' }}>이곳을 클릭하여 사진을 업로드하세요</p>
                  <p style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>JPG, PNG 지원 (최대 10MB)</p>
                </div>
              )}
              <input type="file" ref={fileInputRef} onChange={handleFileChange} hidden accept="image/*" />
            </div>
          </div>

          <h2 className="card-title" style={{ borderBottom: '1px solid #334155', paddingBottom: '1rem', marginTop: '2.5rem' }}>
            <Globe size={24} /> Step 2. 타겟 최적화 설정
          </h2>

          <div className="form-group" style={{ marginTop: '1.5rem' }}>
            <label>배포 채널 (Channel)</label>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              {[
                { id: 'instagram', icon: <Instagram size={18} />, label: '인스타그램' },
                { id: 'twitter', icon: <Twitter size={18} />, label: '트위터' },
                { id: 'blog', icon: <BookOpen size={18} />, label: '블로그' }
              ].map(item => (
                <button 
                  key={item.id}
                  onClick={() => setPlatform(item.id)}
                  style={{ 
                    flex: 1, 
                    display: 'flex', 
                    flexDirection: 'column', 
                    alignItems: 'center', 
                    gap: '0.5rem',
                    padding: '1rem 0.5rem',
                    background: platform === item.id ? '#3b82f6' : '#1e293b',
                    border: '1px solid #334155',
                    borderRadius: '12px'
                  }}
                >
                  {item.icon}
                  <span style={{ fontSize: '0.8rem' }}>{item.label}</span>
                </button>
              ))}
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
            <div className="form-group">
              <label>말투 (Tone)</label>
              <select value={tone} onChange={e => setTone(e.target.value)} style={{ height: '45px' }}>
                <option value="friendly">친근한 / 캐주얼</option>
                <option value="professional">전문적인 / 신뢰감</option>
                <option value="emotional">감성적인 / 따뜻한</option>
              </select>
            </div>
            <div className="form-group">
              <label>언어 (Language)</label>
              <select value={lang} onChange={e => setLang(e.target.value)} style={{ height: '45px' }}>
                <option value="ko">한국어 (Korean)</option>
                <option value="en">영어 (English)</option>
                <option value="jp">일본어 (Japanese)</option>
              </select>
            </div>
          </div>

          <button onClick={createJob} disabled={loading} style={{ height: '60px', fontSize: '1.2rem', marginTop: '2rem', borderRadius: '14px', boxShadow: '0 4px 6px -1px rgba(59, 130, 246, 0.5)' }}>
            {loading ? <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}><Loader2 className="spin" /> 생성 중...</div> : 'AI 마케팅 콘텐츠 생성하기'}
          </button>
        </aside>

        {/* Right: Results Area */}
        <main>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h2 style={{ fontSize: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <List size={24} /> 작업 리스트 ({jobs.length})
            </h2>
          </div>
          
          <div className="job-list">
            {jobs.length === 0 && (
              <div style={{ padding: '6rem 2rem', textAlign: 'center', color: '#64748b', background: '#1e293b', borderRadius: '24px', border: '2px dashed #334155' }}>
                <Sparkles size={48} style={{ margin: '0 auto 1.5rem', opacity: 0.2 }} />
                <p style={{ fontSize: '1.1rem' }}>아직 생성된 콘텐츠가 없습니다.</p>
                <p style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>왼쪽에서 사진을 업로드하고 마케팅 자동화를 시작하세요!</p>
              </div>
            )}
            {jobs.map(job => (
              <div key={job.job_id} className={`job-item ${job.status}`} style={{ padding: '1.75rem', marginBottom: '1.5rem', borderRadius: '20px', background: '#1e293b' }}>
                <div className="job-header">
                  <div style={{ width: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                      <span style={{ fontSize: '1rem', fontWeight: 800, color: '#3b82f6' }}>{job.task === 'marketing_pipeline' ? '🚀 MULTI-CHANNEL AD' : 'JOB'}</span>
                      <span className={`badge badge-${job.status}`} style={{ padding: '0.4rem 0.8rem' }}>
                        {job.status === 'done' ? '생성 완료' : 
                         job.status === 'failed' ? '실패' : 
                         job.pipeline_step === 'analyzing_image' ? '1단계: 이미지 분석' : 
                         job.pipeline_step === 'generating_copy' ? '2단계: 문구 생성' : '대기 중'}
                      </span>
                    </div>
                    
                    {job.status === 'done' && job.result && (
                      <div className="mockup-container" style={{ marginTop: '1.5rem', background: '#fff', borderRadius: '16px', color: '#000', overflow: 'hidden', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.3)' }}>
                        {/* Fake Mobile UI Header */}
                        <div style={{ padding: '0.75rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', borderBottom: '1px solid #efefef' }}>
                          <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888)' }}></div>
                          <span style={{ fontWeight: 700, fontSize: '0.85rem' }}>AI_Marketing_Bot</span>
                        </div>
                        
                        {/* Content Area */}
                        <div style={{ padding: '1.25rem' }}>
                          <p style={{ fontSize: '1rem', lineHeight: 1.5, marginBottom: '1rem', whiteSpace: 'pre-wrap' }}>
                            {job.result.marketing.ad_copy}
                          </p>
                          <p style={{ color: '#00376b', fontSize: '0.95rem' }}>
                            {job.result.marketing.hashtags}
                          </p>
                        </div>
                        
                        {/* Fake Interaction Bar */}
                        <div style={{ padding: '0.75rem 1rem', borderTop: '1px solid #efefef', display: 'flex', gap: '1rem' }}>
                          <Heart size={20} /> <MessageCircle size={20} /> <Send size={20} />
                        </div>
                      </div>
                    )}
                    
                    {job.status === 'running' && (
                      <div style={{ marginTop: '2rem', textAlign: 'center' }}>
                         <Loader2 className="spin" size={32} color="#3b82f6" style={{ margin: '0 auto 1rem' }} />
                         <p style={{ color: '#94a3b8' }}>AI가 최고의 콘텐츠를 고민하고 있습니다...</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
      
      <style>{`
        .spin { animation: spin 1s linear infinite; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .job-item { transition: all 0.3s ease; border: 1px solid #334155; }
        .job-item.done { border-color: #10b981; }
        .job-item:hover { transform: scale(1.02); }
        button { transition: all 0.2s ease; }
        button:active { transform: scale(0.95); }
      `}</style>
    </div>
  );
}
