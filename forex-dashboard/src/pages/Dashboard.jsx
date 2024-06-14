import React, { useState } from 'react'

import { PAIRS } from '../app/data'
import { GRANULARITIES } from '../app/data'
import endPoints from '../app/api'
import Button from '../components/Button'
import Select from '../components/Select'
import Technicals from '../components/Technicals'
import TitleHead from '../components/TitleHead'


function Dashboard() {
  const [selectedPair, setSelectedPair] = useState(PAIRS[0].value);
  const [selectedGranularity, setSelectedGranularity] = useState(GRANULARITIES[0].value);
  const [selectedTechnical, setSelectedTechnical] = useState(null);

  const loadTechnicals = async () => {
    const data = await endPoints.technicals(selectedPair);
    console.log({...data});
    setSelectedTechnical(data)
  }

  return (
    <div>
      <TitleHead title='Options' />

      <div className="segment options">
        <Select name='Currency' title='Select currency' options={PAIRS} defaultValue={selectedPair} onSelected={setSelectedPair} />
        <Select name='Granularity' title='Select granularity' options={GRANULARITIES} defaultValue={selectedGranularity} onSelected={setSelectedGranularity} />

        <Button text='Load' handleClick={() => loadTechnicals()} />
      </div>

      <TitleHead title='Technicals' />
      { selectedTechnical && <Technicals data={selectedTechnical} /> }

    </div>
  )
}

export default Dashboard