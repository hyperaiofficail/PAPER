import React, { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [tools, setTools] = useState([])
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [selectedTool, setSelectedTool] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState(null)

  // Input states
  const [textInput, setTextInput] = useState('')
  const [fileInput, setFileInput] = useState(null)

  useEffect(() => {
    fetchTools()
  }, [])

  const fetchTools = async () => {
    try {
      const res = await axios.get('/api/tools')
      setTools(res.data)
      const cats = ['All', ...new Set(res.data.map(t => t.category).filter(Boolean))]
      setCategories(cats)
    } catch (err) {
      console.error("Failed to fetch tools", err)
    }
  }

  const handleToolClick = (tool) => {
    setSelectedTool(tool)
    setResult(null)
    setTextInput('')
    setFileInput(null)
  }

  const handleCloseModal = () => {
    setSelectedTool(null)
  }

  const handleProcess = async () => {
    if (!selectedTool) return
    setProcessing(true)
    setResult(null)

    const formData = new FormData()
    if (fileInput) {
      formData.append('file', fileInput)
    }
    if (textInput) {
      formData.append('text_input', textInput)
    }

    try {
      const res = await axios.post(`/api/process/${selectedTool.tool_name}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setResult(res.data)
    } catch (err) {
      console.error("Processing failed", err)
      setResult({ status: 'error', message: 'Processing failed. Please try again.' })
    } finally {
      setProcessing(false)
    }
  }

  const filteredTools = selectedCategory === 'All'
    ? tools
    : tools.filter(t => t.category === selectedCategory)

  return (
    <div className="container">
      <h1>100 Tools Dashboard</h1>

      <div className="categories">
        {categories.map(cat => (
          <button
            key={cat}
            className={`category-btn ${selectedCategory === cat ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      <div className="grid">
        {filteredTools.map(tool => (
          <div key={tool.tool_name} className="card" onClick={() => handleToolClick(tool)}>
            <h3>{tool.tool_name}</h3>
            <div className="tags">
                <span className="tag">{tool.category}</span>
            </div>
            <p>{tool.description}</p>
          </div>
        ))}
      </div>

      {selectedTool && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
                <div>
                  <h2 style={{margin: 0}}>{selectedTool.tool_name}</h2>
                  <small style={{color: '#777'}}>{selectedTool.category}</small>
                </div>
                <button className="close-btn" onClick={handleCloseModal}>&times;</button>
            </div>

            <p><strong>Description:</strong> {selectedTool.description}</p>
            <p><strong>Use Case:</strong> {selectedTool.use_case}</p>

            {selectedTool.capabilities && selectedTool.capabilities.length > 0 && (
                <div>
                    <div className="section-label">Capabilities</div>
                    <div className="tags">
                        {selectedTool.capabilities.map((c, i) => <span key={i} className="tag">{c}</span>)}
                    </div>
                </div>
            )}

             {selectedTool.limitations && selectedTool.limitations.length > 0 && (
                <div>
                    <div className="section-label">Limitations</div>
                    <div className="tags">
                        {selectedTool.limitations.map((c, i) => <span key={i} className="tag" style={{background: '#fee', color: '#622', borderColor: '#edd'}}>{c}</span>)}
                    </div>
                </div>
            )}

            <div style={{marginTop: '20px', borderTop: '1px solid #eee', paddingTop: '20px'}}>
                <div className="section-label">Input ({selectedTool.input_type})</div>

                {/* Heuristic to decide whether to show text area or file input */}
                {(selectedTool.input_type.toLowerCase().includes('text') ||
                  selectedTool.input_type.toLowerCase().includes('url') ||
                  selectedTool.input_type === 'Any' ||
                  selectedTool.tool_name.toLowerCase().includes('text') ||
                  selectedTool.tool_name.toLowerCase().includes('qr')
                 ) && (
                    <div className="input-group">
                        <textarea
                            rows="4"
                            placeholder="Enter text or URL here..."
                            value={textInput}
                            onChange={e => setTextInput(e.target.value)}
                        />
                    </div>
                )}

                {/* Heuristic to show file input */}
                {(!selectedTool.input_type.toLowerCase().includes('text') ||
                  selectedTool.input_type === 'Any' ||
                  selectedTool.input_type.includes('/')) && (
                    <div className="input-group">
                        <label>Upload File</label>
                        <input
                            type="file"
                            onChange={e => setFileInput(e.target.files[0])}
                        />
                    </div>
                )}

                <button
                    className="process-btn"
                    onClick={handleProcess}
                    disabled={processing}
                >
                    {processing ? 'Processing...' : 'Process'}
                </button>
            </div>

            {result && (
                <div className="result-box">
                    <h3>Output ({selectedTool.output_type})</h3>
                    {result.status === 'success' ? (
                        <div>
                            <p>{result.message}</p>
                            {result.output && (
                                <div className="result-content">{result.output}</div>
                            )}
                            {result.download_url && (
                                <a href={result.download_url} download style={{display: 'inline-block', marginTop: '10px', color: '#007bff'}}>Download Result</a>
                            )}
                        </div>
                    ) : (
                        <p style={{color: 'red'}}>{result.message}</p>
                    )}
                </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
