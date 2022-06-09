using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Xabe.FFmpeg;
using Xabe.FFmpeg.Downloader;

namespace Core
{
    public class VideoSplittingService : IVideoSplittingService
    {
        public async Task<string> OpenFileAsync(string fileName)
        {
            await FFmpegDownloader.GetLatestVersion(FFmpegVersion.Official);
            await Task.Run(() => SplitVideoToSlides(fileName));
            
            return "/Users/maximvolk/Downloads/img.png";
        }

        private async Task SplitVideoToSlides(string fileName)
        {
            var info = await FFmpeg.GetMediaInfo(fileName).ConfigureAwait(false);
            var videoStream = info.VideoStreams.First()?.SetCodec(VideoCodec.png);

            Func<string, string> outputFileNameBuilder = (number) =>
            {
                return Path.Combine("/Users/maximvolk/Lecture1", $"slide_{number}.png");
            };
            var conversionResult = await FFmpeg.Conversions.New()
                .AddStream(videoStream)
                .ExtractEveryNthFrame(30, outputFileNameBuilder)
                .Start();
        }
    }
}
