import React, { useState } from 'react';

const DataTable = ({ data }) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  if (!data || !data.columns || !data.rows) {
    return null;
  }

  const handleSort = (columnIndex) => {
    let direction = 'asc';
    if (sortConfig.key === columnIndex && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key: columnIndex, direction });
  };

  const sortedRows = [...data.rows].sort((a, b) => {
    if (sortConfig.key === null) return 0;
    
    const aVal = a[sortConfig.key];
    const bVal = b[sortConfig.key];
    
    // Handle numeric values
    const aNum = parseFloat(aVal);
    const bNum = parseFloat(bVal);
    
    if (!isNaN(aNum) && !isNaN(bNum)) {
      return sortConfig.direction === 'asc' ? aNum - bNum : bNum - aNum;
    }
    
    // Handle string values
    const aStr = String(aVal).toLowerCase();
    const bStr = String(bVal).toLowerCase();
    
    if (aStr < bStr) return sortConfig.direction === 'asc' ? -1 : 1;
    if (aStr > bStr) return sortConfig.direction === 'asc' ? 1 : -1;
    return 0;
  });

  const getSortIcon = (columnIndex) => {
    if (sortConfig.key !== columnIndex) {
      return <span className="sort-icon">↕️</span>;
    }
    return sortConfig.direction === 'asc' ? 
      <span className="sort-icon active">↑</span> : 
      <span className="sort-icon active">↓</span>;
  };

  return (
    <div className="data-table-container">
      <div className="table-header">
        <h3>Data Table</h3>
        <div className="table-info">
          {data.rows.length} records
        </div>
      </div>
      
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {data.columns.map((column, index) => (
                <th 
                  key={index} 
                  onClick={() => handleSort(index)}
                  className="sortable-header"
                >
                  <div className="header-content">
                    <span>{column}</span>
                    {getSortIcon(index)}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedRows.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((cell, cellIndex) => (
                  <td key={cellIndex}>
                    {typeof cell === 'string' && cell.includes('%') ? (
                      <div className="percentage-cell">
                        <span className="percentage-value">{cell}</span>
                        <div 
                          className="percentage-bar"
                          style={{ width: cell.replace('%', '') + '%' }}
                        ></div>
                      </div>
                    ) : (
                      cell
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {data.rows.length > 10 && (
        <div className="table-footer">
          <p>Showing all {data.rows.length} records</p>
        </div>
      )}
    </div>
  );
};

export default DataTable;