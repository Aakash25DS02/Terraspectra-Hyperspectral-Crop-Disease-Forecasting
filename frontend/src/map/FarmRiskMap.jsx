import { useMemo } from 'react'
import Map from 'react-map-gl/mapbox'
import DeckGL from '@deck.gl/react'
import { GeoJsonLayer } from '@deck.gl/layers'
import 'mapbox-gl/dist/mapbox-gl.css'

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN

const farmZones = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: {
        zone: 'Zone A',
        risk: 'healthy',
        score: 18
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[
          [76.900, 11.020],
          [76.910, 11.020],
          [76.910, 11.030],
          [76.900, 11.030],
          [76.900, 11.020]
        ]]
      }
    },
    {
      type: 'Feature',
      properties: {
        zone: 'Zone B',
        risk: 'moderate',
        score: 52
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[
          [76.910, 11.020],
          [76.920, 11.020],
          [76.920, 11.030],
          [76.910, 11.030],
          [76.910, 11.020]
        ]]
      }
    },
    {
      type: 'Feature',
      properties: {
        zone: 'Zone C',
        risk: 'high',
        score: 87
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[
          [76.900, 11.030],
          [76.910, 11.030],
          [76.910, 11.040],
          [76.900, 11.040],
          [76.900, 11.030]
        ]]
      }
    },
    {
      type: 'Feature',
      properties: {
        zone: 'Zone D',
        risk: 'healthy',
        score: 22
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[
          [76.910, 11.030],
          [76.920, 11.030],
          [76.920, 11.040],
          [76.910, 11.040],
          [76.910, 11.030]
        ]]
      }
    }
  ]
}

function getRiskColor(risk) {
  if (risk === 'high') {
    return [220, 70, 70, 150]
  }

  if (risk === 'moderate') {
    return [230, 180, 50, 150]
  }

  return [70, 160, 90, 150]
}

export default function FarmRiskMap() {
  const layers = useMemo(() => {
    return [
      new GeoJsonLayer({
        id: 'farm-risk-zones',
        data: farmZones,
        filled: true,
        stroked: true,
        getFillColor: (feature) =>
          getRiskColor(feature.properties.risk),
        getLineColor: [255, 255, 255, 220],
        getLineWidth: 3,
        lineWidthMinPixels: 2,
        pickable: true,

        onClick: ({ object }) => {
          if (object) {
            alert(
              `${object.properties.zone}: ${object.properties.risk} risk (${object.properties.score}%)`
            )
          }
        }
      })
    ]
  }, [])

  const initialViewState = {
    longitude: 76.910,
    latitude: 11.030,
    zoom: 14,
    pitch: 35,
    bearing: 0
  }

  if (!MAPBOX_TOKEN) {
    return (
      <div className="map-error">
        <h3>Mapbox Token Required</h3>

        <p>
          Add your Mapbox access token to the frontend
          environment configuration.
        </p>
      </div>
    )
  }

  return (
    <div className="farm-map">
      <DeckGL
        initialViewState={initialViewState}
        controller={true}
        layers={layers}
      >
        <Map
          mapboxAccessToken={MAPBOX_TOKEN}
          mapStyle="mapbox://styles/mapbox/satellite-streets-v12"
        />
      </DeckGL>

      <div className="map-overlay">
        <h4>Farm Disease Risk</h4>

        <div className="legend-item">
          <span className="legend-color healthy"></span>
          Healthy
        </div>

        <div className="legend-item">
          <span className="legend-color moderate"></span>
          Moderate Risk
        </div>

        <div className="legend-item">
          <span className="legend-color high"></span>
          High Risk
        </div>
      </div>
    </div>
  )
}