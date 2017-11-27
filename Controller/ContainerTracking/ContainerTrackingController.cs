using System;
using System.Drawing;
using System.IO;
using System.Diagnostics;
using System.Data.SqlClient;
using System.Configuration;

namespace ContainerTracking
{
    class ContainerTrackingController
    {
        static void Main(string[] args)
        {
            //take picture and get camera id 
            //create new camera object
            //Assuming you all can put all of your methods and requirements there and just access them like this
            Camera camera = new Camera();

            //store cameraID and image in variables
            //temporary values until camera is working
            Image i = Image.FromFile("D://Programming//Git//ContainerTracking//ImageToText//label1.png");
            int cameraID = 1;

            //call Python application to extract text
            String label = extractText(i);

            //create new container object
            Container container = new Container();

            //query database for container info 
            container = getContainerInfo(cameraID, label);

            //run rules logic on it 

            //display message 
        }

        public static String extractText(Image i)
        {
            string labelText;
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "D://Python//Python36//python.exe"; //cmd is full path to python.exe
            start.Arguments = "D://Programming//Git//ContainerTracking//ImageToText//ExtractText.py"; //args is path to .py file and any cmd line args
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    labelText = reader.ReadLine();
                    Console.Write(labelText);
                }
            }

            return labelText;
        }

        public static Container getContainerInfo(int cameraID, String containerID)
        {
            //create connection string
            var con = ConfigurationManager.ConnectionStrings["INSERT CONNECTION STRING"].ToString();

            //create instance of container and set its containerID and cameraID
            Container container = new Container();
            container.cameraID = cameraID;
            container.containerID = containerID;

            //create the query string, open the connection, and set the status and action
            //NOTE: there may be other fields you want to do here, I just set up the skeleton of it
            using (SqlConnection myConnection = new SqlConnection(con))
            {
                string oString = "Select * from Database where containerID = @containerID and cameraID = @cameraID";
                SqlCommand oCMD = new SqlCommand(oString, myConnection);
                oCMD.Parameters.AddWithValue("@containerID", containerID);
                myConnection.Open();

                using (SqlDataReader oReader = oCMD.ExecuteReader())
                {
                    while (oReader.Read())
                    {
                        container.status = oReader["Status"].ToString();
                        container.action = oReader["Action"].ToString();
                    }
                }
            }


            return container;
        }
    }
}
