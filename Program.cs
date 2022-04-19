using System;
using Renci.SshNet;
using IronPython.Hosting;
using System.IO;
using System.Diagnostics;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            //Connection information
            string user = "lexinclu";
            string pass = "lsm";
            string host = "143.198.73.255";

            string pathRemote = "/gamedata/test.txt";
            string pathLocalFile = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "codigos_nucleares.txt");
            //doPython();
            run_cmd();

            //Se puede hacer sincronicamente o asincronicamente en otro hilo
            //using (SftpClient sftp = new SftpClient(host, 9907, user, pass))
            //{
            //    try
            //    {
            //        sftp.Connect();

            //        Console.WriteLine("Downloading {0}", pathRemote);

            //        using (Stream fileStream = File.OpenWrite(pathLocalFile))
            //        {
            //            sftp.DownloadFile(pathRemote, fileStream);
            //        }

            //        sftp.Disconnect();
            //    }
            //    catch (Exception er)
            //    {
            //        Console.WriteLine("Se ha detectado una excepción " + er.ToString());
            //    }
            //}
          
        }

        private static void run_cmd()
        {
            var cmd = @"C:\Python310\python.exe";
            string arg1 = "Juan";
            string arg = string.Format(@"D:\juan-\Documents\Computacion\Proyecto\SSHtest\prueba.py {0}",arg1);
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = cmd;//cmd is full path to python.exe
            start.Arguments = arg;//args is path to .py file and any cmd line args
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            start.RedirectStandardError = true;
            start.CreateNoWindow = true;

            var errors = "";
            var results = "";

            using (Process process = Process.Start(start))
            {
                errors = process.StandardError.ReadToEnd();
                results = process.StandardOutput.ReadToEnd();

                Console.WriteLine("result:");
                Console.WriteLine(results);
                Console.WriteLine(errors);
            }
       
        }

        private void doPython()
        {
            var engine = Python.CreateEngine();
            var scope = engine.CreateScope();
            var ruta =
                @"def hola(nombre):
                    print (nombre)
                    return True";
            engine.Execute(ruta, scope);
            var saludo = scope.GetVariable("hola");
            var resultado = saludo("alex");
            Console.WriteLine(resultado);
            //ScriptEngine engine = Python.CreateEngine();
            //engine.ExecuteFile(@"D:\juan-\Documents\Computacion\Proyecto\SSHtest\prueba.py");
        }


        
        private static void TakePhoto()
        {

        }

    }

}
