import React from 'react';
import './SearchBar.css';

const SearchBar = ({ onSearch, onFilterChange }) => {
  return (
    <div className="search-bar">
      <input type="text" placeholder="Search" onChange={onSearch} />
      <div className="filters">
        <button onClick={() => onFilterChange('High-Sus')}>High-Sus</button>
        <button onClick={() => onFilterChange('Med-Sus')}>Med-Sus</button>
        <button onClick={() => onFilterChange('Low-Sus')}>Low-Sus</button>
        <button onClick={() => onFilterChange('All')}>All</button>
      </div>
    </div>
  );
};

export default SearchBar;
