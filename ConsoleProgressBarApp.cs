
using System;
using System.Threading;

public class ConsoleProgressBarApp
{
    // Progress bar in console application
    public static void Main()
    {
        int i = 50;
        int total = 500;
        do
        {
            ProgressBar(i, total);
            i++;
            Thread.Sleep(50);
        } while (i <= total);

        Console.ReadLine();
    }

    private static void ProgressBar(int completedProgress, int total)
    {
        int progressBarSize = 20;
        Console.CursorLeft = 0;
        Console.Write("[");
        Console.CursorLeft = progressBarSize;
        Console.Write("]");
        Console.CursorLeft = 1;
        float completedPercentage = ((float)progressBarSize / total) * completedProgress;

        int position = 0;
        for (int i = 1; i < completedPercentage; i++)
        {
            Console.BackgroundColor = ConsoleColor.Green;
            Console.CursorLeft = ++position;
            Console.Write(" ");
        }

        Console.CursorLeft = progressBarSize + 5;
        Console.BackgroundColor = ConsoleColor.Black;
        Console.Write(completedProgress.ToString() + "/" + total.ToString() + "");
    }

    public static void RotatingLoader()
    {
        int position = 0;
        while (true)
        {
            position++;
            switch (position % 3)
            {
                case 0: Console.Write("/"); break;
                case 1: Console.Write("-"); break;
                case 2: Console.Write("|"); break;
            }

            Console.CursorLeft = Console.CursorLeft - 1;
            Thread.Sleep(100);
        }
    }

    public static void DotDotLoader(int dotCount = 3)
    {
        while (true)
        {
            int position = 0;
            while (position < dotCount)
            {
                Console.Write(".");
                position++;
                Thread.Sleep(500);
            }

            while (position > 0)
            {
                position--;
                Console.Write("\b \b");
            }
            Thread.Sleep(500);
        }
    }
}
