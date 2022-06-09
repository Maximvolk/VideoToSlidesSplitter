using System.Reactive;
using System.Reactive.Linq;
using System.Threading.Tasks;
using ReactiveUI;
using Core;

namespace Presentation.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        public ReactiveCommand<Unit, Unit> OpenFile { get; }
        public Interaction<Unit, string?> ShowOpenFileDialog { get; }
        public Interaction<string, Unit> OpenFramePreview { get; }

        private readonly IVideoSplittingService _service = new VideoSplittingService();

        public MainWindowViewModel()
        {
            OpenFile = ReactiveCommand.CreateFromTask(OpenFileAsync);
            ShowOpenFileDialog = new Interaction<Unit, string?>();
            OpenFramePreview = new Interaction<string, Unit>();
        }

        private async Task OpenFileAsync()
        {
            var videoFilePath = await ShowOpenFileDialog.Handle(Unit.Default);
            if (videoFilePath == null)
                return;

            var frameFilePath = await _service.OpenFileAsync(videoFilePath);
            await OpenFramePreview.Handle(frameFilePath);
        }

        public void RemoveFile()
        {
            
        }
    }
}
