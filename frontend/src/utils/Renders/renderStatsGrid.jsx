import '../../styles/statsGrid.css';

function renderStatsGrid(json) {
  return (json?.map(
    course => {
      return (<>
              <div className='item div-course-name'>
                {course.text}
              </div>
              <div className="item div-abit-rank" style={{textAlign:"center"}}>
                {course.groups?.map(group => { return (<div style={{ margin: "10px 0" }}>{group}</div>) })}
              </div>
              <div className="item div-unfold-info" style={{textAlign:"center", cursor:"pointer"}}>
                Подробнее &#8595;
              </div>
              </>);
    }
  ));
}

export default renderStatsGrid;