import '../../styles/statsGrid.css';

function renderStatsGrid(json) {
  return (json?.map(
    course => {
      return (<>
              <div style={{display:'flex', justifyContent:"space-between", width:"70vw"}}>
                {course.text}
                <div className="div-unfold-info" style={{cursor: "pointer"}}>
                    <span>Подробнее &#8595;</span>
                </div>
              </div>
              <div className="grid-stats">
                  <div className='item' >hi</div>
                  <div className='item' >hi</div>
                  {course.groups?.map(elem => { 
                    return (
                      <>
                      <div className='item' >{elem.group}</div>
                      <div className='item' >{elem.pos}</div>
                      </>
                    )})
                  }
              </div>
              </>);
    }
  ));
}

export default renderStatsGrid;