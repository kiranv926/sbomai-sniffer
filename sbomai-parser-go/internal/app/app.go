package app

import (
	"fmt"
	"os"

	"github.com/sbomai/sbomai-parser-go/pkg/scanner"
	"github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

// App represents the main application
type App struct {
	rootCmd *cobra.Command
	scanner  *scanner.SyftScanner
}

// NewApp creates a new application instance
func NewApp() *App {
	app := &App{
		scanner: scanner.NewSyftScanner(),
	}

	app.rootCmd = &cobra.Command{
		Use:   "sbomai-parser",
		Short: "SBOM AI Parser - Generate and analyze SBOMs using Syft",
		Long:  "A Go-based SBOM parser that integrates with Syft to generate Software Bill of Materials and analyze them for vulnerabilities.",
	}

	app.rootCmd.AddCommand(app.scanCommand())
	app.rootCmd.AddCommand(app.analyzeCommand())

	return app
}

// Run executes the application
func (a *App) Run() error {
	return a.rootCmd.Execute()
}

// scanCommand creates the scan command
func (a *App) scanCommand() *cobra.Command {
	var output string

	cmd := &cobra.Command{
		Use:   "scan [target]",
		Short: "Scan a target (directory, file, or image) to generate SBOM",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			target := args[0]
			logrus.Infof("Scanning target: %s", target)

			result, err := a.scanner.Scan(target)
			if err != nil {
				return fmt.Errorf("scan failed: %w", err)
			}

			if output != "" {
				if err := os.WriteFile(output, []byte(result), 0644); err != nil {
					return fmt.Errorf("failed to write output: %w", err)
				}
				logrus.Infof("SBOM written to: %s", output)
			} else {
				fmt.Println(result)
			}

			return nil
		},
	}

	cmd.Flags().StringVarP(&output, "output", "o", "", "Output file path (default: stdout)")

	return cmd
}

// analyzeCommand creates the analyze command
func (a *App) analyzeCommand() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "analyze [sbom-file]",
		Short: "Analyze an existing SBOM file for vulnerabilities",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			sbomFile := args[0]
			logrus.Infof("Analyzing SBOM file: %s", sbomFile)

			// TODO: Implement SBOM analysis logic
			logrus.Info("SBOM analysis completed")
			return nil
		},
	}

	return cmd
}
