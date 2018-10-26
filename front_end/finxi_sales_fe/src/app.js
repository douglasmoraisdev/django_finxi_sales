import React from 'react';
import TopBar from './appcomponents/topbar'
import CenteredTabs from './appcomponents/tabs'
import Footer from './appcomponents/footer'

function App(props) {

  return (
      <div className="root">
        <TopBar />
        <CenteredTabs />
        <Footer />

      </div>
      );
}

export default App;
