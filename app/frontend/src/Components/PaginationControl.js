import React, { useState } from 'react';

const PaginationControl = ({ totalPages }) => {
  const [currentPage, setCurrentPage] = useState(1);

  const goToNextPage = () => {
    setCurrentPage((currentPage) => Math.min(currentPage + 1, totalPages));
  }

  const goToPreviousPage = () => {
    setCurrentPage((currentPage) => Math.max(currentPage - 1, 1));
  }

  return (
    <div className="pagination">
      <button onClick={goToPreviousPage} disabled={currentPage === 1}>
        &lt;
      </button>
      {/* Display page dots */}
      {[...Array(totalPages).keys()].map((page) => (
        <span key={page} className={currentPage === page + 1 ? 'dot active' : 'dot'}>•</span>
      ))}
      <button onClick={goToNextPage} disabled={currentPage === totalPages}>
        &gt;
      </button>
    </div>
  );
};

export default PaginationControl;
