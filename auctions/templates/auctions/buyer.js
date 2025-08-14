import React from 'react'
import { Form,FormControl,Button } from 'react-bootstrap';
import FOOTER from './footer';


 class buyer extends React.Component {


  constructor(){
    super();
  
    this.state = {
      products:null };
  }
componentDidMount(){
fetch('http://127.0.0.1:8000/Listing/?format=json').then((resp)=> {
  resp.json().then((result) => {
    console.warn (result)
  })
})

     }  
      
  render() {
    return (
        <div className="App"  style={{backgroundColor:"#D3D3D3", paddingTop:50}}>
   <div className="container"  >
              <div className='row' >
             <h1 style={{textAlign:'center',marginLeft:320, marginRight:80, color:'	#696969'}}>PRODUCTS</h1>
       <Form inline >
      <FormControl type="text" placeholder="Search Products" className="mr-sm-2"  />
      <Button variant="outline-info">Search </Button>
    </Form>
       </div>
      
   <div className="row" style={{margin:30}}>
   <div class="col-sm">
   <div class="card" >
   <img src="http://www.hamailartgalleries.com/uploads/art/thumb_01f86747c1df996fcf431cf3bedd4e90.jpg" class="card-img-top" alt="..."/>
   <div class="card-body">
   <h5 class="card-title">Card title</h5>
   <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
   <a href="#" class="btn btn-primary">Buy Now</a>
   </div>
   </div>
   </div>
                 
   <div class="col-sm"><div class="card" >
   <img src="http://www.hamailartgalleries.com/uploads/art/thumb_86091a78199546865f8951100aa273ca.JPG" class="card-img-top" alt="..."/>
   <div class="card-body">
   <h5 class="card-title">Card title</h5>
   <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
   <a href="#" class="btn btn-primary">Buy Now</a>
   </div>
   </div></div>
 
   <div class="col-sm"><div class="card" >
   <img src="http://www.hamailartgalleries.com/uploads/art/thumb_b538fc99314f01b5b3cb3c97097825a4.JPG" class="card-img-top" alt="..."/>
   <div class="card-body">
   <h5 class="card-title">Card title</h5>
   <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
   <a href="#" class="btn btn-primary">Buy Now</a>
   </div>
   </div></div>
   
 
 
     </div>
     
     <div className="row"style={{margin:30}}>
     <div class="col-sm"><div class="card" >
   <img src="http://www.hamailartgalleries.com/uploads/art/thumb_86091a78199546865f8951100aa273ca.JPG" class="card-img-top" alt="..."/>
   <div class="card-body">
   <h5 class="card-title">Card title</h5>
   <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
   <a href="#" class="btn btn-primary">Buy Now</a>
   </div>
   </div></div>
 
   <div class="col-sm"><div class="card" >
   <img src="http://www.hamailartgalleries.com/uploads/art/thumb_b538fc99314f01b5b3cb3c97097825a4.JPG" class="card-img-top" alt="..."/>
   <div class="card-body">
   <h5 class="card-title">Card title</h5>
   <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
   <a href="#" class="btn btn-primary">Buy Now</a>
   </div>
   </div></div>
   <div class="col-sm"><div class="card" >
   <img src="http://www.hamailartgalleries.com/uploads/art/thumb_b538fc99314f01b5b3cb3c97097825a4.JPG" class="card-img-top" alt="..."/>
   <div class="card-body">
   <h5 class="card-title">Card title</h5>
   <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
   <a href="#" class="btn btn-primary">Buy Now</a>
   </div>
   </div></div>
   
     </div>
     <br/><br/><br/><br/><br/><br/>
     

     </div>
     <FOOTER/>
     </div>
    );
    }
}
export default buyer;