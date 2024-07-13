const flaskUrl = "http://localhost:5000"

export default async function request(url, method = 'GET', data = null) {
    try 
    {  

      const jwtToken = localStorage.getItem('jwtToken');
      const headers = {};
      if (jwtToken) 
      {
          headers['Authorization'] = `Bearer ${jwtToken}`;
      }
      headers['Content-Type'] = "application/json"
      const response = await fetch(flaskUrl + url, 
        {
          method,
          headers:headers,
          body: data ? JSON.stringify(data) : null,
        });
        if (!response.ok) 
        {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const responseData = await response.json();
        return { success: true, data: responseData };
    } 
    catch (error) 
    {
        return { success: false, error: 'Failed to fetch data. '+ error };
    }
  }

 