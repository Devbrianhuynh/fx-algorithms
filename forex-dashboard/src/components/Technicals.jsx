import React from 'react'

import Progress from './Progress'


const HEADERS = [
    'r1', 'r2', 'r3',
    's1', 's2', 's3',
    'pivot'
]

function Technicals({ data }) {
  return (
    <div className='segment'>

        {/* Not available */}
        <Progress title='Bullish' color='#21BA45' percentage={data.percent_bullish} />
        <Progress title='Bearish' color='#DB2828' percentage={data.percent_bearish} />

        <table>
            <thead>

                <tr>{
                    HEADERS.map((item) => {
                        return <th key={item}>{item}</th>
                    })
                    }
                </tr>

                <tr>{
                    HEADERS.map((item) => {
                        return <th key={item}>{data[item]}</th>
                    })
                    }
                </tr>
                
            </thead>
        </table>

    </div>
  )
}

export default Technicals