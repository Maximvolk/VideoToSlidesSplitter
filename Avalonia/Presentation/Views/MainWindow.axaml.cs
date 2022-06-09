using System.Reactive;
using System.Linq;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.ReactiveUI;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using ReactiveUI;
using Presentation.ViewModels;

namespace Presentation.Views
{
    public partial class MainWindow : ReactiveWindow<MainWindowViewModel>
    {
        public MainWindow()
        {
            InitializeComponent();

            this.WhenActivated(d => d(ViewModel.ShowOpenFileDialog.RegisterHandler(ShowOpenFileDialog)));
            this.WhenActivated(d => d(ViewModel.OpenFramePreview.RegisterHandler(OpenFramePreview)));
        }

        private async Task ShowOpenFileDialog(InteractionContext<Unit, string?> interaction)
        {
            var dialog = new OpenFileDialog();

            var fileNames = await dialog.ShowAsync(this);
            interaction.SetOutput(fileNames.FirstOrDefault());
        }

        private async Task OpenFramePreview(InteractionContext<string, Unit> interaction)
        {
            var previewPanel = this.Get<Panel>("PreviewPanel");
            previewPanel.Background = new ImageBrush(new Bitmap(interaction.Input));

            interaction.SetOutput(Unit.Default);
        }
    }
}
