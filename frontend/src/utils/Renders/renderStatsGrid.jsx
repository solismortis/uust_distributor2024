import '../../styles/statsGrid.css';

function renderStatsGrid(json) {
  return (json?.map(
    course => {
      return (<>
              <div className='item div-course-name'>
                {course.title}
              </div>
              <div className="item div-abit-rank" style={{textAlign:"center"}}>
                Ваша позиция: 1
              </div>
              <div className="item div-unfold-info" style={{textAlign:"center", cursor:"pointer"}}>
                Подробнее &#8595;
              </div>
              </>);
    }
  ));
}

export default renderStatsGrid;